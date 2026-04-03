import streamlit as st
import pandas as pd

# 1. PEGA ACÁ LA URL DE TU EXCEL (La que ves en el navegador)
URL_EXCEL = "https://docs.google.com/spreadsheets/d/1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10/edit?gid=883227529#gid=883227529"

# Función para convertir la URL normal en una de descarga de datos
def obtener_url_csv(sheet_name):
    base_url = URL_EXCEL.replace("/edit", "")
    return f"{base_url}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

st.title("🏆 PRODE MUNDIAL 2026")

tab1, tab2 = st.tabs(["⚽ Cargar Goles", "📊 Posiciones"])

with tab1:
    st.header("Cargá tu pronóstico")
    usuario = st.text_input("Tu Nombre:")
    
    # Leemos los partidos directamente de la URL pública
    try:
        df_partidos = pd.read_csv(obtener_url_csv("Partidos"))
        lista = df_partidos['equipo_local'] + " vs " + df_partidos['equipo_visitante']
        partido = st.selectbox("Partido:", lista)
        
        # Goles
        c1, c2 = st.columns(2)
        g_l = c1.number_input("Goles Local", min_value=0, step=1)
        g_v = c2.number_input("Goles Visitante", min_value=0, step=1)

        if st.button("Enviar Pronóstico"):
            st.warning("⚠️ Para guardar, hacé clic en el link de abajo y pegá los datos (es la forma más simple sin errores de seguridad)")
            # Esto genera un link que le manda los datos al Excel si usas un Formulario, 
            # pero por ahora, para no marearte, vamos a ver si lee el Ranking.
            st.write(f"Voto de {usuario}: {partido} -> {g_l}-{g_v}")
    except:
        st.error("No se pudo leer el Excel. Revisá que sea 'Público'.")

with tab2:
    st.header("🏆 Tabla de Posiciones")
    try:
        # Leemos la pestaña de cálculos
        df_ranking = pd.read_csv(obtener_url_csv("CalculoPuntos"))
        # Sumamos los puntos
        resumen = df_ranking.groupby("Usuario")["Puntos"].sum().reset_index()
        resumen = resumen.sort_values(by="Puntos", ascending=False)
        
        st.table(resumen)
    except:
        st.info("Todavía no hay puntos cargados.")
