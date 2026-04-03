import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")
ID_SHEET = "1BACdwjatWM8mpPKSAOXY8I3IP-MecfJgyqa7OSZWTO"

def conectar_google():
    try:
        # Esto busca la sección [gcp_service_account] en tus Secrets
        info_llave = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(info_llave, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error en los Secrets: {e}")
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
                st.warning("Poné tu nombre.")

    with t2:
        st.header("🏆 Posiciones")
        try:
            ws_rank = spreadsheet.worksheet("CalculoPuntos")
            df_r = pd.DataFrame(ws_rank.get_all_records())
            df_r = df_r.dropna(subset=['Usuario', 'Puntos'])
            res = df_r.groupby("Usuario")["Puntos"].sum().reset_index()
            st.table(res.sort_values("Puntos", ascending=False))
        except:
            st.info("No hay puntos cargados aún.")

except Exception as e:
    st.error("Error de conexión con Google.")
    st.info("Revisá que el mail de tu JSON sea Editor en el Excel.")
