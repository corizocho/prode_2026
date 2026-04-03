import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

# --- CONEXIÓN CON GOOGLE SHEETS ---
# El ID de tu Excel (sacado de la URL)
ID_SHEET = "1BACdwjatWM8mpPKSAOXY8I3IP-MecfJgyqa7OSZWTO"

def conectar_google():
    # Lee la "llave" desde los Secrets de Streamlit
    creds_dict = st.secrets["gcp_service_account"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

# --- INICIO DE LA APP ---
try:
    # Conectamos al Excel
    client = conectar_google()
    spreadsheet = client.open_by_key(1BACdwjatWM8mpPKSAOXY8I3IP-MecfJgyqa7OSZWTO)
    
    st.title("🏆 PRODE MUNDIAL 2026")

    # Creamos las pestañas
    tab_prode, tab_ranking = st.tabs(["⚽ Cargar Goles", "📊 Tabla de Posiciones"])

    # --- PESTAÑA 1: CARGA DE PRONÓSTICOS ---
    with tab_prode:
        st.header("Cargá tu pronóstico")
        
        usuario = st.text_input("Tu Nombre (ej: nicolas, edu):")
        
        # Leemos la pestaña 'Partidos' para armar el selector
        ws_partidos = spreadsheet.worksheet("Partidos")
        df_partidos = pd.DataFrame(ws_partidos.get_all_records())
        
        # Armamos la lista para que el usuario elija
        lista_nombres = df_partidos['equipo_local'] + " vs " + df_partidos['equipo_visitante']
        partido_elegido = st.selectbox("Seleccioná el partido:", lista_nombres)
        
        # Buscamos el ID del partido seleccionado
        idx = lista_nombres.tolist().index(partido_elegido)
        id_partido = df_partidos.iloc[idx]['id']
        
        # Inputs de goles
        col1, col2 = st.columns(2)
        with col1:
            goles_l = st.number_input("Goles Local", min_value=0, step=1, key="g_local")
        with col2:
            goles_v = st.number_input("Goles Visitante", min_value=0, step=1, key="g_visit")
            
        if st.button("Enviar Pronóstico"):
            if usuario:
                try:
                    # Escribimos en 'Respuestas de formulario 1'
                    ws_respuestas = spreadsheet.worksheet("Respuestas de formulario 1")
                    # Formato: Marca temporal, Usuario, ID Partido, Goles L, Goles V
                    fecha_actual = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')
                    ws_respuestas.append_row([fecha_actual, usuario, id_partido, goles_l, goles_v])
                    
                    st.success(f"✅ ¡Excelente {usuario}! Pronóstico guardado.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
            else:
                st.warning("⚠️ Por favor, ingresá tu nombre antes de enviar.")

    # --- PESTAÑA 2: RANKING ---
    with tab_ranking:
        st.header("🏆 Tabla de Posiciones")
        
        try:
            # Leemos la pestaña donde están tus fórmulas mágicas
            ws_puntos = spreadsheet.worksheet("CalculoPuntos")
            df_puntos = pd.DataFrame(ws_puntos.get_all_records())
            
            if not df_puntos.empty:
                # Agrupamos por usuario y sumamos los puntos
                # Asegurate que en el Excel las columnas se llamen 'Usuario' y 'Puntos'
                ranking = df_puntos.groupby("Usuario")["Puntos"].sum().reset_index()
                ranking = ranking.sort_values(by="Puntos", ascending=False).reset_index(drop=True)
                
                # Mostramos la tabla
                st.table(ranking)
                
                if not ranking.empty:
                    puntero = ranking.iloc[0]['Usuario']
                    st.info(f"🥇 El puntero actual es: **{puntero}**")
            else:
                st.write("Todavía no hay datos de puntos.")
                
        except Exception as e:
            st.info("Esperando que se procesen los puntos en el Excel...")

except Exception as
