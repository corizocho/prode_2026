import streamlit as st
import pandas as pd
import requests
import json

# --- CONFIGURACIÓN ---
SHEET_ID = "1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10"
# Tu URL de Apps Script actualizada
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxilAcoq93UZ7ahSxK5u2E20iCwKQ7umBtRBa4Q86oKq4_upzlMNFrTIZCO9xGDmcGvYA/exec"

st.set_page_config(page_title="Prode 2026", page_icon="⚽", layout="wide")
st.title("🏆 Mi Prode Amigos 2026")

# --- CARGA DE DATOS ---
url_partidos = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Partidos"

try:
    df_partidos = pd.read_csv(url_partidos)
    nombres = ["Juan", "Pedro", "Maria", "Corizocho", "nicolas", "edu"] 
    usuario = st.sidebar.selectbox("¿Quién sos?", ["Seleccionar..."] + nombres)

    if usuario != "Seleccionar...":
        st.header(f"Fixture para {usuario}")
        st.info("Cargá tus goles y usá el botón de abajo para guardar todo de una vez.")
        
        pronosticos_lista = []
        
        # Generamos el fixture visualmente
        for index, row in df_partidos.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 0.5, 1, 3])
                
                with col1: 
                    st.write(f"### {row['equipo_local']}")
                with col2: 
                    g_l = st.number_input("", min_value=0, step=1, key=f"l_{row['id']}", label_visibility="collapsed")
                with col3: 
                    st.write("## -")
                with col4: 
                    g_v = st.number_input("", min_value=0, step=1, key=f"v_{row['id']}", label_visibility="collapsed")
                with col5: 
                    st.write(f"### {row['equipo_visitante']}")
                
                # Armamos el paquete de datos para este partido
                pronosticos_lista.append({
                    "usuario": usuario,
                    "id_partido": int(row['id']),
                    "goles_l": int(g_l),
                    "goles_v": int(g_v)
                })
            st.divider()

        # Botón único para guardar todo el fixture
        if st.button("🚀 GUARDAR TODOS MIS PRONÓSTICOS"):
            with st.spinner("Enviando datos al Excel..."):
                try:
                    # Enviamos la lista completa como JSON
                    response = requests.post(SCRIPT_URL, data=json.dumps(pronosticos_lista))
                    
                    if "Éxito" in response.text:
                        st.success("¡Golazo! Se guardaron todos los resultados correctamente.")
                        st.balloons()
                    else:
                        st.error()
