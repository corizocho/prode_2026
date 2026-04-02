import streamlit as st
from st_gsheets_connection import GSheetsConnection

# Configuración básica
st.set_page_config(page_title="Prode Mundial 2026", page_icon="⚽")
st.title("🏆 Prode Amigos 2026")

# Intentar conectar al Google Sheet
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.success("¡Conectado al Prode!")
    
    # Aquí es donde el usuario elegiría su nombre
    usuario = st.sidebar.selectbox("¿Quién sos?", ["Elegir...", "Juan", "Pedro", "Maria"])
    
    if usuario != "Elegir...":
        st.write(f"Bienvenido, **{usuario}**. Cargá tus resultados:")
        # Ejemplo visual de partido
        col1, col2, col3 = st.columns([2,1,2])
        with col1: st.write("🇲🇽 México")
        with col2: st.number_input("", min_value=0, max_value=20, key="m1", label_visibility="collapsed")
        with col3: st.write("🇵🇱 Polonia")
        
        if st.button("Guardar Predicción"):
            st.balloons()
            st.info("Predicción enviada (simulación)")

except Exception as e:
    st.error("Falta configurar la conexión al Sheet en Streamlit Cloud.")
    st.info("Una vez que la app cargue, pasame el link de tu Google Sheet y te digo dónde pegar el ID.")
