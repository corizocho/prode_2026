import streamlit as st
import pandas as pd
from gsheetsdb import connect

# Configuración de la página
st.set_page_config(page_title="Prode Mundial 2026", page_icon="⚽")

st.title("🏆 Prode Amigos - Mundial 2026")

# --- LOGIN ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

with st.sidebar:
    st.header("Ingreso")
    usuario = st.selectbox("Seleccioná tu nombre", ["Juan", "Pedro", "Maria"]) # Esto lo leeremos del Sheet después
    pin = st.text_input("PIN de 4 dígitos", type="password")
    if st.button("Entrar"):
        # Lógica de validación (simplificada para el ejemplo)
        st.session_state.autenticado = True
        st.session_state.usuario = usuario
        st.success(f"Hola {usuario}!")

if st.session_state.autenticado:
    tab1, tab2 = st.tabs(["⚽ Cargar Pronósticos", "📊 Tabla de Posiciones"])

    with tab1:
        st.subheader("Tus Predicciones")
        # Aquí generamos la lista de partidos
        # Simulando un partido:
        st.write("---")
        col1, col2, col3 = st.columns([2,1,2])
        with col1: st.write("🇲🇽 México")
        with col2: goles_l = st.number_input("Goles", min_value=0, max_value=15, key="l1", step=1)
        with col3: st.write("🇵🇱 Polonia")
        
        # En el código final, esto guardará directamente en el Google Sheet
        if st.button("Guardar Pronósticos"):
            st.success("¡Pronósticos guardados correctamente!")

    with tab2:
        st.subheader("Ranking General")
        # Simulación de tabla
        data = {"Jugador": ["Juan", "Maria", "Pedro"], "Puntos": [12, 10, 8]}
        df_ranking = pd.DataFrame(data)
        st.table(df_ranking.sort_values(by="Puntos", ascending=False))

else:
    st.info("Por favor, ingresá tu nombre y PIN en la barra lateral para participar.")
