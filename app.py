import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

ID_SHEET = "1BACdwjatwM8mpPkSAOXY8I3IP-MecfjgYqa7OSZw10"

# Estas URLs son las más robustas para leer hojas específicas por nombre
URL_PARTIDOS = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/gviz/tq?tqx=out:csv&sheet=Partidos"
URL_RANKING = f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/gviz/tq?tqx=out:csv&sheet=CalculoPuntos"

st.title("🏆 PRODE MUNDIAL 2026")

t1, t2 = st.tabs(["⚽ Pronósticos", "📊 Posiciones"])

with t1:
    st.header("Cargá tu jugada")
    try:
        # Importante: La línea de abajo tiene que tener 4 espacios de sangría
        df_p = pd.read_csv(URL_PARTIDOS)
        
        # Limpiamos nombres de columnas por si hay espacios invisibles en el Excel
        df_p.columns = df_p.columns.str.strip()
        
        nombre = st.text_input("Tu Nombre:")
        
        # Armamos la lista de partidos
        opciones = df_p['equipo_local'] + " vs " + df_p['equipo_visitante']
        sel = st.selectbox("Elegí el partido:", opciones)
        
        st.divider()
        st.info("🎯 Para anotar tus goles, hacelo en el Excel mientras terminamos el botón.")
        st.link_button("Ir al Excel para anotar", f"https://docs.google.com/spreadsheets/d/{ID_SHEET}/edit")
        
    except Exception as e:
        st.error("No se pudo cargar la lista de partidos.")
        st.write(f"Error técnico: {e}")

with t2:
    st.header("🏆 Tabla de Posiciones")
    try:
        df_r = pd.read_csv(URL_RANKING)
        df_r.columns = df_r.columns.str.strip()
        
        if not df_r.empty:
            # Agrupamos por usuario y sumamos puntos
            res = df_r.groupby("Usuario")["Puntos"].sum().reset_index()
            st.table(res.sort_values("Puntos", ascending=False).reset_index(drop=True))
        else:
            st.info("Sin puntos cargados todavía.")
    except Exception as e:
        st.error("No se pudo leer el ranking.")
