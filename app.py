import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")
ID_SHEET = "1BACdwjatwM8mpPkSAOXY8l3IP-MecfjgYqa7OSZw10"

def conectar():
    try:
        s = st.secrets["gcp_service_account"]
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
        st.error(f"Error de llaves: {e}")
        return None

client = conectar()

if client:
    try:
        sheet = client.open_by_key(ID_SHEET)
        st.title("🏆 PRODE MUNDIAL 2026")
        
        t1, t2 = st.tabs(["⚽ Cargar Pronóstico", "📊 Tabla de Posiciones"])

        with t1:
            st.header("Cargá tus resultados")
            ws_p = sheet.worksheet("Partidos")
            df_p = pd.DataFrame(ws_p.get_all_records())
            
            nombre = st.text_input("Tu Nombre:")
            opciones = df_p['equipo_local'] + " vs " + df_p['equipo_visitante']
            sel = st.selectbox("Elegí el partido:", opciones)
            
            # Obtener ID del partido
            id_p = df_p.iloc[opciones.tolist().index(sel)]['id']
            
            c1, c2 = st.columns(2)
            g_l = c1.number_input("Goles Local", min_value=0, step=1)
            g_v = c2.number_input("Goles Visitante", min_value=0, step=1)
            
            if st.button("Guardar Pronóstico"):
                if nombre:
                    ws_res = sheet.worksheet("Respuestas de formulario 1")
                    # Esto escribe en el Excel y el usuario se queda en la web
                    ws_res.append_row([pd.Timestamp.now().strftime('%d/%m/%Y %H:%M'), nombre, id_p, g_l, g_v])
                    st.success("✅ ¡Pronóstico guardado correctamente!")
                    st.balloons()
                else:
                    st.warning("Por favor, ingresá tu nombre.")

        with t2:
            st.header("🏆 Posiciones")
            ws_r = sheet.worksheet("CalculoPuntos")
            df_r = pd.DataFrame(ws_r.get_all_records())
            if not df_r.empty:
                res = df_r.groupby("Usuario")["Puntos"].sum().reset_index()
                st.table(res.sort_values("Puntos", ascending=False).reset_index(drop=True))
            else:
                st.info("No hay puntos calculados aún.")

    except Exception as e:
        st.error(f"Error de conexión con la planilla: {e}")
