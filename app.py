import streamlit as st
import pandas as pd
import requests

# --- CONFIGURACIÓN ---
SHEET_ID = "1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10"
# Link de envío del formulario
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe-N62t_1nQAK08u0Orr23Zk5fu69vo34chTa229CCiQx5mQA/formResponse"

st.set_page_config(page_title="Prode 2026", page_icon="⚽")
st.title("🏆 Mi Prode 2026")

# Función para mandar datos al Google Form de forma invisible
def enviar_a_google(user, id_p, g_l, g_v):
    datos = {
        "entry.331238612": user,       # Usuario
        "entry.1706692557": id_p,      # ID Partido
        "entry.1741549419": g_l,       # Goles Local
        "entry.1351187424": g_v        # Goles Visitante
    }
    try:
        requests.post(FORM_URL, data=datos)
    except:
        pass

# --- CARGA DE DATOS ---
url_partidos = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Partidos"

try:
    df_partidos = pd.read_csv(url_partidos)
    
    # Login en el lateral
    nombres = ["Juan", "Pedro", "Maria", "Corizocho", "Invitado"] 
    usuario = st.sidebar.selectbox("¿Quién sos?", ["Seleccionar..."] + nombres)

    if usuario != "Seleccionar...":
        st.header(f"Hola {usuario}, cargá tus resultados:")
        
        # Diccionario para guardar lo que escribe el usuario antes de apretar el botón
        resultados_temp = {}

        # Mostramos los partidos (filtramos los que no tienen resultado real)
        partidos_vivos = df_partidos[df_partidos['goles_local_real'].isna()]

        for index, row in partidos_vivos.iterrows():
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 1, 0.5, 1, 2])
                with col1: st.write(f"**{row['equipo_local']}**")
                with col2: res_l = st.number_input("L", min_value=0, step=1, key=f"l_{row['id']}", label_visibility="collapsed")
                with col3: st.write("-")
                with col4: res_v = st.number_input("V", min_value=0, step=1, key=f"v_{row['id']}", label_visibility="collapsed")
                with col5: st.write(f"**{row['equipo_visitante']}**")
                
                # Guardamos en memoria temporal
                resultados_temp[row['id']] = (res_l, res_v)
            st.write("---")

        if st.button("🚀 GUARDAR TODO EN EL EXCEL"):
            with st.spinner('Guardando tus pronósticos...'):
                for id_p, (gl, gv) in resultados_temp.items():
                    enviar_a_google(usuario, id_p, gl, gv)
                
                st.success("¡Listo! Tus resultados ya están en el Excel.")
                st.balloons()

except Exception as e:
    st.error("Error de conexión. Asegurate de que el Sheet esté Público.")
