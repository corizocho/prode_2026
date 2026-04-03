import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

# --- CONEXIÓN CON GOOGLE SHEETS ---
# EL ID TIENE QUE IR ENTRE COMILLAS SÍ O SÍ
ID_SHEET = "1BACdwjatWM8mpPKSAOXY8I3IP-MecfJgyqa7OSZWTO"

def conectar_google():
    try:
        # Lee los Secrets que pegaste en el panel de Streamlit
        creds_dict = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error("Error en Secrets: Revisá que la llave JSON esté bien pegada.")
        st.stop()

# --- INICIO DE LA APP ---
try:
    client = conectar_google()
    spreadsheet = client.open_by_key(ID_SHEET)
    
    st.title("🏆 PRODE MUNDIAL 2026")

    tab1, tab2 = st.tabs(["⚽ Cargar Goles", "📊 Tabla de Posiciones"])

    with tab1:
        st.header("Cargá tu pronóstico")
        usuario = st.text_input("Tu Nombre (como figura en el Prode):")
        
        # Leemos los partidos
        ws_partidos = spreadsheet.worksheet("Partidos")
        df_partidos = pd.DataFrame(ws_partidos.get_all_records())
        
        lista = df_partidos['equipo_local'] + " vs " + df_partidos['equipo_visitante']
        partido_sel = st.selectbox("Seleccioná el partido:", lista)
        
        idx = lista.tolist().index(partido_sel)
        id_p = df_partidos.iloc[idx]['id']
        
        c1, c2 = st.columns(2)
        g_l = c1.number_input("Goles Local", min_value=0, step=1, key="gl")
        g_v = c2.number_input("Goles Visitante", min_value=0, step=1, key="gv")
        
        if st.button("Enviar Pronóstico"):
            if usuario:
                ws_res = spreadsheet.worksheet("Respuestas de formulario 1")
                ahora = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')
                ws_res.append_row([ahora, usuario, id_p, g_l, g_v])
                st.success(f"✅ ¡Cargado {usuario}! Ya se ve en el Excel.")
                st.balloons()
            else:
                st.warning("Poné tu nombre primero.")

    with tab2:
        st.header("🏆 Posiciones")
        try:
            ws_puntos = spreadsheet.worksheet("CalculoPuntos")
            df_p = pd.DataFrame(ws_puntos.get_all_records())
            
            if not df_p.empty:
                # Agrupamos por usuario y sumamos puntos
                ranking = df_p.groupby("Usuario")["Puntos"].sum().reset_index()
                ranking = ranking.sort_values(by="Puntos", ascending=False).reset_index(drop=True)
                st.table(ranking)
            else:
                st.info("Todavía no hay puntos procesados.")
        except:
            st.write("Cargando ranking...")

except Exception as e:
    st.error("Fallo la conexión con el Excel.")
    st.write(f"Error técnico: {e}")
    st.info("💡 Recordá: Compartí el Excel con el mail de tu JSON como 'Editor'.")
