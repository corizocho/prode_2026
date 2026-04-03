import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

ID_SHEET = "1BACdwjatwM8mpPkSAOXY8I3IP-MecfjgYqa7OSZw10"

# REEMPLAZÁ LOS NÚMEROS DE ABAJO POR LOS QUE ANOTASTE
# Si 'Partidos' es la primera pestaña, suele ser 0
GID_PARTIDOS = "0" 
# Buscá el de CalculoPuntos en la URL de tu Excel
GID_RANKING = "883227529" 

URL_PARTIDOS = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid={GID_PARTIDOS}"
URL_RANKING = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid={GID_RANKING}"

st.title("🏆 PRODE MUNDIAL 2026")

t1, t2 = st.tabs(["⚽ Pronósticos", "📊 Posiciones"])

with t1:
    st.header("Cargá tu jugada")
    try:
        df_p = pd.read_csv(URL_PARTIDOS)
        df_p.columns = df_p.columns.str.strip()
        
        nombre = st.text_input("Tu Nombre:")
        
        # Unimos las columnas para el selector
        opciones = df_p['equipo_local'] + " vs " + df_p['equipo_visitante']
        sel = st.selectbox("Elegí el partido:", opciones)
        
        st.divider()
        st.info("🎯 Para anotar goles, hacelo en el Excel por ahora.")
        st.link_button("Ir al Excel", f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/edit")
        
    except Exception as e:
        st.error("No se pudo cargar la lista de partidos.")
        st.write(f"Error: {e}")

with t2:
    st.header("🏆 Tabla de Posiciones")
    try:
        df_r = pd.read_csv(URL_RANKING)
        df_r.columns = df_r.columns.str.strip()
        if not df_r.empty:
            res = df_r.groupby("Usuario")["Puntos"].sum().reset_index()
            st.table(res.sort_values("Puntos", ascending=False).reset_index(drop=True))
        else:
            st.info("Sin puntos cargados.")
    except:
        st.error("No se pudo leer el ranking.")
