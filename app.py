import streamlit as st
import pandas as pd

st.set_page_config(page_title="Prode Mundial 2026", page_icon="⚽")
st.title("🏆 Prode Amigos 2026")

# TU LINK DE GOOGLE SHEETS (Versión Exportar)
sheet_id = "1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10"
url_partidos = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Partidos"

try:
    # Leemos los datos directamente
    df_partidos = pd.read_csv(url_partidos)
    
    st.success("¡Conectado con éxito!")
    
    # Menú lateral para elegir usuario
    nombres_amigos = ["Juan", "Pedro", "Maria", "Corizocho"] # Después lo levantamos del Sheet
    usuario = st.sidebar.selectbox("¿Quién sos?", ["Seleccionar..."] + nombres_amigos)

    if usuario != "Seleccionar...":
        st.subheader(f"Hola {usuario}, cargá tus pronósticos:")
        
        # Mostramos solo los primeros 3 partidos de prueba
        for index, row in df_partidos.head(3).iterrows():
            col1, col2, col3 = st.columns([2,1,2])
            with col1: st.write(row['equipo_local'])
            with col2: st.number_input("Goles", min_value=0, key=f"l_{index}", label_visibility="collapsed")
            with col3: st.write(row['equipo_visitante'])
            
        if st.button("Guardar todo"):
            st.balloons()
            st.warning("Para guardar de verdad, necesitamos un paso final de escritura, ¡pero la app ya funciona!")

except Exception as e:
    st.error("Error al leer el Sheet. Asegurate de que el Sheet esté 'Público' (Cualquier persona con el enlace puede ver).")
    st.info(f"Detalle técnico: {e}")
