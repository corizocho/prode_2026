import streamlit as st
import pandas as pd
from gspread_streamlit import get_gspread_client

# --- CONFIGURACIÓN INICIAL ---
SHEET_ID = "https://docs.google.com/spreadsheets/d/1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10/edit?gid=883227529#gid=883227529" # <--- ACORDATE DE PONER TU ID

st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

# Conexión con Google Sheets
client = get_gspread_client()
spreadsheet = client.open_by_key(SHEET_ID)

# --- FUNCIÓN PARA GUARDAR DATOS ---
def guardar_pronostico(usuario, id_partido, goles_l, goles_v):
    try:
        sheet = spreadsheet.worksheet("Respuestas de formulario 1")
        sheet.append_row([usuario, id_partido, goles_l, goles_v])
        return True
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        return False

# --- INTERFAZ ---
st.title("🏆 PRODE MUNDIAL 2026")

tab_prode, tab_ranking = st.tabs(["⚽ Cargar Goles", "📊 Tabla de Posiciones"])

with tab_prode:
    st.header("Cargá tu pronóstico")
    usuario = st.text_input("Ingresá tu nombre:")
    
    url_partidos = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Partidos"
    try:
        df_partidos = pd.read_csv(url_partidos)
        lista_nombres = df_partidos['equipo_local'] + " vs " + df_partidos['equipo_visitante']
        partido_elegido = st.selectbox("Seleccioná el partido:", lista_nombres)
        
        idx = lista_nombres.tolist().index(partido_elegido)
        id_partido = df_partidos.iloc[idx]['id']
        
        col1, col2 = st.columns(2)
        with col1:
            goles_l = st.number_input("Goles Local", min_value=0, step=1, key="l")
        with col2:
            goles_v = st.number_input("Goles Visitante", min_value=0, step=1, key="v")
            
        if st.button("Enviar Pronóstico"):
            if usuario:
                if guardar_pronostico(usuario, id_partido, goles_l, goles_v):
                    st.success("✅ ¡Pronóstico cargado!")
            else:
                st.warning("Poné tu nombre.")
    except:
        st.error("Error al leer partidos.")

with tab_ranking:
    st.header("🏆 Posiciones")
    url_ranking = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=CalculoPuntos"
    
    try:
        df_ranking = pd.read_csv(url_ranking)
        # Limpiamos filas vacías por si las moscas
        df_ranking = df_ranking.dropna(subset=['Usuario', 'Puntos'])
        resumen = df_ranking.groupby("Usuario")["Puntos"].sum().reset_index()
        resumen = resumen.sort_values(by="Puntos", ascending=False).reset_index(drop=True)
        
        st.table(resumen)
        
        if not resumen.empty:
            puntero = resumen.iloc[0]['Usuario']
            st.info(f"🥇 El puntero es: **{puntero}**")
            if st.button("Tirar papelitos"):
                st.balloons()
    except:
        st.info("Todavía no hay puntos.")
