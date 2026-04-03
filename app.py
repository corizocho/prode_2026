import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURACIÓN DE SEGURIDAD ---
# Esto lee la "llave" que vamos a pegar en Secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def conectar_google():
    creds_dict = st.secrets["gcp_service_account"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

# --- INTERFAZ ---
st.title("🏆 PRODE MUNDIAL 2026")

ID_SHEET = "1BACdwjatWM8mpPKSAOXY8I3IP-MecfJgyqa7OSZWTO"

try:
    client = conectar_google()
    sheet = client.open_by_key(ID_SHEET)
    
    tab1, tab2 = st.tabs(["⚽ Cargar Goles", "📊 Posiciones"])

    with tab1:
        st.header("Cargá tu pronóstico")
        usuario = st.text_input("Tu Nombre:")
        
        # Leer Partidos
        ws_partidos = sheet.worksheet("Partidos")
        df_partidos = pd.DataFrame(ws_partidos.get_all_records())
        
        lista = df_partidos['equipo_local'] + " vs " + df_partidos['equipo_visitante']
        partido_sel = st.selectbox("Partido:", lista)
        idx = lista.tolist().index(partido_sel)
        id_p = df_partidos.iloc[idx]['id']

        c1, c2 = st.columns(2)
        g_l = c1.number_input("Goles Local", min_value=0, step=1)
        g_v = c2.number_input("Goles Visitante", min_value=0, step=1)

        if st.button("Enviar Pronóstico"):
            if usuario:
                ws_res = sheet.worksheet("Respuestas de formulario 1")
                ws_res.append_row([pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'), usuario, id_p, g_l, g_v])
                st.success("✅ ¡Pronóstico guardado automáticamente!")
            else:
                st.error("Poné tu nombre.")

    with tab2:
        st.header("🏆 Tabla de Posiciones")
        ws_puntos = sheet.worksheet("CalculoPuntos")
        df_puntos = pd.DataFrame(ws_puntos.get_all_records())
        
        if not df_puntos.empty:
            resumen = df_puntos.groupby("Usuario")["Puntos"].sum().reset_index()
            resumen = resumen.sort_values(by="Puntos", ascending=False).reset_index(drop=True)
            st.table(resumen)

except Exception as e:
    st.error(f"Falta configurar la llave en Secrets: {e}")
