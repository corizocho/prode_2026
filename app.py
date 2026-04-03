import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")
ID_SHEET = "1BACdwjatwM8mpPkSAOXY8l3IP-MecfjgYqa7OSZw10"

def conectar_google():
    try:
        s = st.secrets["gcp_service_account"]
        # Limpiamos la llave por las dudas
        pk = s["private_key"].replace("\\n", "\n").strip()
        
        info = {
            "type": s["type"],
            "project_id": s["project_id"],
            "private_key_id": s["private_key_id"],
            "private_key": pk,
            "client_email": s["client_email"],
            "client_id": s["client_id"],
            "auth_uri": s["auth_uri"],
            "token_uri": s["token_uri"],
            "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
            "client_x509_cert_url": s["client_x509_cert_url"]
        }
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error de llave: {e}")
        st.stop()

# --- APP ---
try:
    client = conectar_google()
    spreadsheet = client.open_by_key(ID_SHEET)
    
    st.title("🏆 PRODE MUNDIAL 2026")
    t1, t2 = st.tabs(["⚽ Cargar Goles", "📊 Posiciones"])

    with t1:
        st.header("Cargá tu pronóstico")
        nombre = st.text_input("Tu Nombre:")
        ws_p = spreadsheet.worksheet("Partidos")
        df_p = pd.DataFrame(ws_p.get_all_records())
        opciones = df_p['equipo_local'] + " vs " + df_p['equipo_visitante']
        sel = st.selectbox("Partido:", opciones)
        id_partido = df_p.iloc[opciones.tolist().index(sel)]['id']
        
        c1, c2 = st.columns(2)
        g_l = c1.number_input("Goles Local", min_value=0, step=1, key="l")
        g_v = c2.number_input("Goles Vis", min_value=0, step=1, key="v")
        
        if st.button("Enviar"):
            if nombre:
                ws_res = spreadsheet.worksheet("Respuestas de formulario 1")
                ws_res.append_row([pd.Timestamp.now().strftime('%d/%m/%Y %H:%M'), nombre, id_partido, g_l, g_v])
                st.success("✅ ¡Guardado!")
                st.balloons()
            else:
                st.warning("Falta el nombre.")

    with t2:
        st.header("🏆 Posiciones")
        try:
            ws_rank = spreadsheet.worksheet("CalculoPuntos")
            df_r = pd.DataFrame(ws_rank.get_all_records())
            df_r = df_r[df_r['Usuario'] != ""]
            res = df_r.groupby("Usuario")["Puntos"].sum().reset_index()
            st.table(res.sort_values("Puntos", ascending=False).reset_index(drop=True))
        except:
            st.info("Sin puntos aún.")

except Exception as e:
    st.error("Error de red con Google. Intentando reconectar...")
    st.write(f"Detalle: {e}")
