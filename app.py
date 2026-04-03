import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

# --- CONFIGURACIÓN ---
ID_SHEET = "1BACdwjatwM8mpPkSAOXY8I3IP-MecfjgYqa7OSZw10"

# Estas URLs son "mágicas": fuerzan a Google a darte los datos sin pedir llaves
URL_PARTIDOS = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid=0"
URL_RANKING = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/export?format=csv&gid=883227529"

st.title("🏆 PRODE MUNDIAL 2026")

t1, t2 = st.tabs(["⚽ Pronósticos", "📊 Posiciones"])

with t1:
    st.header("Cargá tu jugada")
    try:
        # Usamos pandas para leer la URL pública
        df_p = pd.read_csv(URL_PARTIDOS)
        
        if not df_p.empty:
            nombre = st.text_input("Tu Nombre:")
            # Verificá que las columnas se llamen exactamente así en tu Excel
            opciones = df_p['equipo_local'] + " vs " + df_p['equipo_visitante']
            sel = st.selectbox("Elegí el partido:", opciones)
            
            st.info("💡 Para anotar los goles, hacelo en el Excel mientras terminamos de conectar el botón.")
            st.markdown(f"[👉 Abrir planilla para anotar](https://docs.google.com/spreadsheets/d/{ID_SHEET}/edit)")
        else:
            st.warning("La hoja 'Partidos' parece estar vacía.")
    except Exception as e:
        st.error("No se pudo conectar con la hoja de Partidos.")
        st.write(f"Error técnico: {e}")

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
