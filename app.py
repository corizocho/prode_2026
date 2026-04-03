import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

# URL de tu Google Sheet (la que usás siempre)
URL_SHEET = "https://docs.google.com/spreadsheets/d/1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10/edit?gid=883227529#gid=883227529"

# Conexión oficial de Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

# --- INTERFAZ ---
st.title("🏆 PRODE MUNDIAL 2026")

tab_prode, tab_ranking = st.tabs(["⚽ Cargar Goles", "📊 Tabla de Posiciones"])

with tab_prode:
    st.header("Cargá tu pronóstico")
    usuario = st.text_input("Tu Nombre:")
    
    try:
        # Leemos los partidos
        df_partidos = conn.read(spreadsheet=URL_SHEET, worksheet="Partidos")
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
                # Traemos las respuestas actuales y sumamos la nueva
                df_respuestas = conn.read(spreadsheet=URL_SHEET, worksheet="Respuestas de formulario 1")
                nueva_fila = pd.DataFrame({"Marca temporal": [pd.Timestamp.now()], "usuario": [usuario], "id_partido": [id_partido], "goles_local": [goles_l], "goles_visitante": [goles_v]})
                df_actualizado = pd.concat([df_respuestas, nueva_fila], ignore_index=True)
                
                # Guardamos en el Excel
                conn.update(spreadsheet=URL_SHEET, worksheet="Respuestas de formulario 1", data=df_actualizado)
                st.success(f"✅ ¡Cargado {usuario}! Suerte.")
            else:
                st.warning("Escribí tu nombre, che.")
    except Exception as e:
        st.error(f"Error: {e}")

with tab_ranking:
    st.header("🏆 Posiciones")
    try:
        # Leemos la pestaña de cálculos donde ya funcionan tus fórmulas
        df_ranking = conn.read(spreadsheet=URL_SHEET, worksheet="CalculoPuntos", ttl=0) # ttl=0 para que no use caché
        
        # Limpiamos y agrupamos
        df_ranking = df_ranking.dropna(subset=['Usuario', 'Puntos'])
        resumen = df_ranking.groupby("Usuario")["Puntos"].sum().reset_index()
        resumen = resumen.sort_values(by="Puntos", ascending=False).reset_index(drop=True)
        
        st.table(resumen)
        
        if not resumen.empty:
            st.info(f"🥇 El puntero es: **{resumen.iloc[0]['Usuario']}**")
            if st.button("Celebrar"):
                st.balloons()
    except:
        st.info("Todavía no hay puntos cargados.")
