import streamlit as st
import pandas as pd
from gspread_streamlit import get_gspread_client

# --- CONFIGURACIÓN INICIAL ---
# Reemplazá esto con el ID de tu Google Sheet (está en la URL de tu navegador)
SHEET_ID = "https://docs.google.com/spreadsheets/d/1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10/edit?gid=883227529#gid=883227529"

st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

# Conexión con Google Sheets
client = get_gspread_client()
spreadsheet = client.open_by_key(SHEET_ID)

# --- FUNCIÓN PARA GUARDAR DATOS ---
def guardar_pronostico(usuario, id_partido, goles_l, goles_v):
    try:
        # IMPORTANTE: El nombre de la pestaña debe ser igual al del Excel
        sheet = spreadsheet.worksheet("Respuestas de formulario 1")
        # Guardamos: Usuario, ID Partido, Goles Local, Goles Visitante
        sheet.append_row([usuario, id_partido, goles_l, goles_v])
        return True
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        return False

# --- INTERFAZ DE USUARIO ---
st.title("🏆 PRODE MUNDIAL 2026")

# Creamos las pestañas para organizar la app
tab_prode, tab_ranking = st.tabs(["⚽ Cargar Goles", "📊 Tabla de Posiciones"])

# --- PESTAÑA 1: CARGA DE DATOS ---
with tab_prode:
    st.header("Cargá tu pronóstico")
    
    usuario = st.text_input("Ingresá tu nombre (como figura en el Prode):")
    
    # Traemos los partidos de la pestaña 'Partidos' para el selector
    url_partidos = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Partidos"
    try:
        df_partidos = pd.read_csv(url_partidos)
        lista_nombres = df_partidos['equipo_local'] + " vs " + df_partidos['equipo_visitante']
        
        partido_elegido = st.selectbox("Seleccioná el partido:", lista_nombres)
        
        # Obtenemos el ID real del partido seleccionado
        idx = lista_nombres.tolist().index(partido_elegido)
        id_partido = df_partidos.iloc[idx]['id']
        
        col1, col2 = st.columns(2)
        with col1:
            goles_l = st.number_input("Goles Local", min_value=0, step=1, key="l")
        with col2:
            goles_v = st.number_input("Goles Visitante", min_value=0, step=1, key="v")
            
        if st.button("Enviar Pronóstico"):
            if usuario:
                exito = guardar_pronostico(usuario, id_partido, goles_l, goles_v)
                if exito:
                    st.success(f"✅ ¡Listo {usuario}! Cargado el {goles_l}-{goles_v} para el partido {id_partido}.")
            else:
                st.warning("Poné tu nombre antes de enviar, boludo.")
    except:
        st.error("No pude leer la pestaña 'Partidos'. Revisá el nombre en el Excel.")

# --- PESTAÑA 2: RANKING ---
with tab_ranking:
    st.header("🏆 Posiciones en Tiempo Real")
    
    # URL de la pestaña de cálculos donde hicimos las fórmulas
    url_ranking = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=CalculoPuntos"
    
    try:
        df_ranking = pd.read_csv(url_ranking)
        
        # Agrupamos por usuario y sumamos los puntos
        # Asegurate que en tu Excel la columna se llame 'Usuario' y la otra 'Puntos'
        resumen = df_ranking.groupby("Usuario")["Puntos"].sum().reset_index()
        resumen = resumen.sort_values(by="Puntos", ascending=False).reset_index(drop=True)
        
        # Mostramos el Ranking
        st.dataframe(resumen, use_container_width=True)
        
        if not resumen.empty:
            puntero = resumen.iloc[0]['Usuario']
            st.balloons() if st
