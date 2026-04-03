import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

# --- CONFIGURACIÓN ---
ID_SHEET = "1BACdwjatwM8mpPkSAOXY8I3IP-MecfjgYqa7OSZw10"

# Estas URLs usan el nombre de la hoja directamente (sheet=Nombre)
URL_PARTIDOS = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/gviz/tq?tqx=out:csv&sheet=Partidos"
URL_RANKING = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/gviz/tq?tqx=out:csv&sheet=CalculoPuntos"

st.title("🏆 PRODE MUNDIAL 2026")

t1, t2 = st.tabs(["⚽ Pronósticos", "📊 Posiciones"])

with t1:
    st.header("Cargá tu jugada")
    try:
        # Leemos los partidos
        df_p = pd.read_csv(URL_PARTIDOS)
        
        # Limpieza rápida por si Google mete columnas vacías
        df_p = df_p.dropna(subset=['equipo_local', 'equipo_visitante'])
        
        nombre = st.text_input("Tu Nombre:", placeholder="Escribí tu nombre acá")
        
        opciones = df_p['equipo_local'] + " vs " + df_p['equipo_visitante']
        sel = st.selectbox("Elegí el partido:", opciones)
        
        st.divider()
        st.info("🎯 Para anotar tus goles, hacelo directamente en el Excel mientras terminamos la conexión del botón.")
        st.link_button("Ir al Excel para anotar", f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/edit")

    except Exception as e:
        st.error("No se pudo cargar la lista de partidos.")
        st.write("Verificá que la pestaña del Excel se llame exactamente 'Partidos'")

with t2:
    st.header("🏆 Tabla de Posiciones")
    try:
        # Lee el ranking directamente del Excel público
        df_r = pd.read_csv(URL_RANKING)
        if not df_r.empty:
            res = df_r.groupby("Usuario")["Puntos"].sum().reset_index()
            st.table(res.sort_values("Puntos", ascending=False).reset_index(drop=True))
        else:
            st.info("Todavía no hay puntos cargados.")
    except:
        st.error("Asegurate de que la hoja 'CalculoPuntos' tenga datos.")
