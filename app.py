import streamlit as st
import pandas as pd
import requests
import time

# --- CONFIGURACIÓN ---
SHEET_ID = "1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe-N62t_1nQAK08u0Orr23Zk5fu69vo34chTa229CCiQx5mQA/formResponse"

st.set_page_config(page_title="Prode 2026", page_icon="⚽")
st.title("🏆 Mi Prode 2026")

def enviar_a_google(user, id_p, g_l, g_v):
    datos = {
        "entry.331238612": user,
        "entry.1706692557": id_p,
        "entry.1741549419": g_l,
        "entry.1351187424": g_v
    }
    try:
        # Agregamos un 'timeout' para que no se quede colgado
        response = requests.post(FORM_URL, data=datos, timeout=10)
        return response.status_code
    except:
        return 404

# --- CARGA DE DATOS ---
url_partidos = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Partidos"

try:
    df_partidos = pd.read_csv(url_partidos)
    nombres = ["Juan", "Pedro", "Maria", "Corizocho", "nicolas"] 
    usuario = st.sidebar.selectbox("¿Quién sos?", ["Seleccionar..."] + nombres)

    if usuario != "Seleccionar...":
        st.header(f"Hola {usuario}")
        votos = {}
        
        # Mostramos los partidos
        for index, row in df_partidos.iterrows():
            with st.container():
                st.write(f"**Partido #{row['id']}**")
                col1, col2, col3, col4, col5 = st.columns([2, 1, 0.5, 1, 2])
                with col1: st.write(row['equipo_local'])
                with col2: l = st.number_input("L", min_value=0, step=1, key=f"l_{row['id']}", label_visibility="collapsed")
                with col3: st.write("-")
                with col4: v = st.number_input("V", min_value=0, step=1, key=f"v_{row['id']}", label_visibility="collapsed")
                with col5: st.write(row['equipo_visitante'])
                votos[row['id']] = (l, v)
            st.write("---")

        if st.button("🚀 GUARDAR TODO"):
            progress_bar = st.progress(0)
            exitos = 0
            total = len(votos)
            
            for i, (id_p, (gl, gv)) in enumerate(votos.items()):
                status = enviar_a_google(usuario, id_p, gl, gv)
                if status == 200:
                    exitos += 1
                
                # Pequeña pausa para no saturar a Google
                time.sleep(0.5)
                progress_bar.progress((i + 1) / total)
            
            if exitos == total:
                st.success(f"¡Golazo! Se guardaron los {exitos} resultados.")
                st.balloons()
            elif exitos > 0:
                st.warning(f"Se guardaron {exitos} de {total}. Reintentá con los que faltan.")
            else:
                st.error("Google nos rechazó el envío. Probá cargando de a 1 o 2 partidos.")

except Exception as e:
    st.error(f"Error técnico: {e}")
