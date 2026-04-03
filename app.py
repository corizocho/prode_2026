import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

# --- CONEXIÓN CON GOOGLE SHEETS ---
# EL ID TIENE QUE IR ENTRE COMILLAS SIEMPRE
ID_SHEET = "1BACdwjatWM8mpPKSAOXY8I3IP-MecfJgyqa7OSZWTO"

def conectar_google():
    try:
        # Lee la "llave" desde los Secrets de Streamlit
        creds_dict = st.secrets["gcp_service_account"]
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error("Error en los Secrets: Asegurate de haber pegado la llave JSON correctamente.")
        st.stop()

# --- INICIO DE LA APP ---
try:
    client = conectar_google()
    # Usamos la variable ID_SHEET que definimos arriba con comillas
    spreadsheet = client.open_by_key("1BACdwjatWM8mpPKSAOXY8I3IP-MecfJgyqa7OSZWTO")
    
    st.title("🏆 PRODE MUNDIAL 2026")

    tab_prode, tab_ranking = st.tabs(["⚽ Cargar Goles", "📊 Tabla de Posiciones"])

    # --- PESTAÑA 1: CARGA DE PRONÓSTICOS ---
    with tab_prode:
        st.header("Cargá tu pronóstico")
        usuario = st.text_input("Tu Nombre (ej: nicolas, edu):")
        
        ws_partidos = spreadsheet.worksheet("Partidos")
        df_partidos = pd.DataFrame(ws_partidos.get_all_records())
        
        lista_nombres = df_partidos['equipo_local'] + " vs " + df_partidos['equipo_visitante']
        partido_elegido = st.selectbox("Seleccioná el partido:", lista_nombres)
        
        idx = lista_nombres.tolist().index(partido_elegido)
        id_partido = df_partidos.iloc[idx]['id']
        
        col1, col2 = st.columns(2)
        with col1:
            goles_l = st.number_input("Goles Local", min_value=0, step=1, key="gl")
        with col2:
            goles_v = st.number_input("Goles Visitante", min_value=0, step=1, key="gv")
            
        if st.button("Enviar Pronóstico"):
            if usuario:
                ws_respuestas = spreadsheet.worksheet("Respuestas de formulario 1")
                fecha = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')
                ws_respuestas.append_row([fecha, usuario, id_partido, goles_l, goles_v])
                st.success(f"✅ ¡Guardado! Suerte {usuario}.")
                st.balloons()
            else:
                st.warning("Escribí tu nombre.")

    # --- PESTAÑA 2: RANKING ---
    with tab_ranking:
        st.header("🏆 Tabla de Posiciones")
        try:
            ws_puntos = spreadsheet.worksheet("CalculoPuntos")
            df_puntos = pd.DataFrame(ws_puntos.get_all_records())
            
            if not df_puntos.empty:
                ranking = df_puntos.groupby("Usuario")["Puntos"].sum().reset_index()
                ranking = ranking.sort_values(by="Puntos", ascending=False).reset_index(drop=True)
                st.table(ranking)
            else:
                st.write("Sin datos todavía.")
        except:
            st.info("Procesando puntos...")

except Exception as e:
    st.error("Fallo la conexión con el Excel.")
    st.write(f"Error técnico: {e}")
    st.info("💡 Recordá: El Excel tiene que estar compartido con el mail de tu JSON como 'Editor'.")
