import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

# Este es el link de tu Excel público transformado para que Python lo lea directo
ID_SHEET = "1BACdwjatwM8mpPkSAOXY8I3IP-MecfjgYqa7OSZw10"
URL_PARTIDOS = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/gviz/tq?tqx=out:csv&sheet=Partidos"
URL_RANKING = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/gviz/tq?tqx=out:csv&sheet=CalculoPuntos"

st.title("🏆 PRODE MUNDIAL 2026")

t1, t2 = st.tabs(["⚽ Pronósticos", "📊 Posiciones"])

with t1:
    st.header("Cargá tu jugada")
    try:
        df_p = pd.read_csv(URL_PARTIDOS)
        nombre = st.text_input("Tu Nombre:")
        opciones = df_p['equipo_local'] + " vs " + df_p['equipo_visitante']
        sel = st.selectbox("Elegí el partido:", opciones)
        
        st.info("Para guardar los goles, usá el formulario de Google Sheets directo mientras arreglamos la escritura automática.")
        st.write("Link al Excel para anotar: [Click aquí](https://docs.google.com/spreadsheets/d/1BACdwjatwM8mpPkSAOXY8l3IP-MecfjgYqa7OSZw10/edit)")
    except:
        st.error("No se pudo leer la lista de partidos.")

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
