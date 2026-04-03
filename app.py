import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")

# --- REEMPLAZÁ ESTOS LINKS CON LOS QUE GENERASTE EN "PUBLICAR EN LA WEB" ---
LINK_CSV_PARTIDOS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR8qz-i8ZF0m9eiH-jPXh7Lv1nvGmjK1a9dFY00U2sdHz7IRux9JPJHNmW-FLsiLOBDJlM9ab2gqvtq/pub?gid=0&single=true&output=csv"
LINK_CSV_RANKING = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR8qz-i8ZF0m9eiH-jPXh7Lv1nvGmjK1a9dFY00U2sdHz7IRux9JPJHNmW-FLsiLOBDJlM9ab2gqvtq/pub?gid=883227529&single=true&output=csv"

st.title("🏆 PRODE MUNDIAL 2026")

# Creamos las pestañas visuales
tab1, tab2 = st.tabs(["⚽ Cargar Pronóstico", "📊 Tabla de Posiciones"])

with tab1:
    st.header("Tu Jugada")
    try:
        # Leemos los datos directamente del link público
        df_p = pd.read_csv(LINK_CSV_PARTIDOS)
        
        # Limpiamos posibles espacios en los nombres de las columnas
        df_p.columns = df_p.columns.str.strip()
        
        nombre = st.text_input("Tu Nombre:", placeholder="Escribí quién sos")
        
        # Armamos la lista de partidos combinando local y visitante
        # Asegurate que las columnas en el Excel se llamen exactamente 'equipo_local' y 'equipo_visitante'
        opciones_partidos = df_p['equipo_local'] + " vs " + df_p['equipo_visitante']
        seleccion = st.selectbox("Elegí el partido que querés pronosticar:", opciones_partidos)
        
        st.divider()
        
        # Mensaje de ayuda mientras resolvemos la escritura automática
        st.info("💡 Por ahora, para que tus goles se sumen, anotalos directamente en la planilla.")
        st.link_button("👉 Abrir Excel para anotar goles", "https://docs.google.com/spreadsheets/d/1BACdwjatwM8mpPkSAOXY8l3IP-MecfjgYqa7USZw10/edit")

    except Exception as e:
        st.error("No se pudo conectar con la lista de partidos.")
        st.write(f"Detalle del error: {e}")

with tab2:
    st.header("🏆 Posiciones Actualizadas")
    try:
        # Leemos la hoja de ranking
        df_r = pd.read_csv(LINK_CSV_RANKING)
        df_r.columns = df_r.columns.str.strip()
        
        if not df_r.empty:
            # Agrupamos por usuario y sumamos los puntos
            # Asegurate que las columnas se llamen 'Usuario' y 'Puntos'
            ranking = df_r.groupby("Usuario")["Puntos"].sum().reset_index()
            ranking = ranking.sort_values(by="Puntos", ascending=False).reset_index(drop=True)
            
            # Mostramos la tabla linda
            st.table(ranking)
        else:
            st.warning("Todavía no hay puntos cargados en la hoja 'CalculoPuntos'.")
            
    except Exception as e:
        st.error("No se pudo cargar la tabla de posiciones.")
        st.write(f"Detalle del error: {e}")

# Pie de página
st.caption("Prode Mundial 2026 - Actualización automática vía Google Sheets")
