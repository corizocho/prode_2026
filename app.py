import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

ID_SHEET = "1BACdwjatwM8mpPkSAOXY8I3IP-MecfjgYqa7OSZw10"

def conectar():
    try:
        s = st.secrets["gcp_service_account"]
        # Limpieza de la llave
        pk = s["private_key"].replace("\\n", "\n").strip()
        
        info = {
            "type": s["type"], "project_id": s["project_id"],
            "private_key_id": s["private_key_id"], "private_key": pk,
            "client_email": s["client_email"], "client_id": s["client_id"],
            "auth_uri": s["auth_uri"], "token_uri": s["token_uri"],
            "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
            "client_x509_cert_url": s["client_x509_cert_url"]
        }
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error de configuración: {e}")
        return None

client = conectar()

if client:
    try:
        sheet = client.open_by_key(ID_SHEET)
        st.title("🏆 PRODE MUNDIAL 2026")
        
        t1, t2 = st.tabs(["⚽ Pronósticos", "📊 Posiciones"])

        with t1:
            ws_p = sheet.worksheet("Partidos")
            df_p = pd.DataFrame(ws_p.get_all_records())
            
            nombre = st.text_input("Tu Nombre:")
            opciones = df_p['equipo_local'] + " vs " + df_p['equipo_visitante']
            sel = st.selectbox("Elegí el partido:", opciones)
            
            # Buscamos el ID del partido seleccionado
            id_partido = df_p.iloc[opciones.tolist().index(sel)]['id']
            
            col1, col2 = st.columns(2)
            g_l = col1.number_input("Goles Local", min_value=0, step=1, key="l")
            g_v = col2.number_input("Goles Vis", min_value=0, step=1, key="v")
            
            if st.button("Guardar Pronóstico"):
                if nombre:
                    ws_res = sheet.worksheet("Respuestas de formulario 1")
                    # Guardamos directo en el Excel sin salir de la app
                    ws_res.append_row([pd.Timestamp.now().strftime('%d/%m/%Y %H:%M'), nombre, id_partido, g_l, g_v])
                    st.success(f"¡Listo {nombre}! Pronóstico guardado.")
                    st.balloons()
                else:
                    st.warning("Poné tu nombre para participar.")

        with t2:
            ws_r = sheet.worksheet("CalculoPuntos")
            df_r = pd.DataFrame(ws_r.get_all_records())
            if not df_r.empty:
                ranking = df_r.groupby("Usuario")["Puntos"].sum().reset_index()
                st.table(ranking.sort_values("Puntos", ascending=False))

    except Exception as e:
        st.error(f"Falla de red con Google: {e}")
        st.info("Reintentá en unos segundos o hacé un 'Reboot App'.")
