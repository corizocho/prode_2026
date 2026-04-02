import streamlit as st
import pandas as pd
import urllib.parse

# --- CONFIGURACIÓN ---
SHEET_ID = "1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10"
# Link base del formulario (termina en /viewform)
BASE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe-N62t_1nQAK08u0Orr23Zk5fu69vo34chTa229CCiQx5mQA/viewform"

st.set_page_config(page_title="Prode 2026", page_icon="⚽")
st.title("🏆 Mi Prode 2026")

# --- CARGA DE DATOS ---
url_partidos = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Partidos"

try:
    df_partidos = pd.read_csv(url_partidos)
    nombres = ["Juan", "Pedro", "Maria", "Corizocho", "nicolas"] 
    usuario = st.sidebar.selectbox("¿Quién sos?", ["Seleccionar..."] + nombres)

    if usuario != "Seleccionar...":
        st.header(f"Hola {usuario}")
        st.info("Cargá tus goles y abajo aparecerá el link para guardar.")
        
        # Por ahora, para no marear, cargamos el Partido #1
        # Si tenés más en el Excel, esto se puede hacer un bucle
        partido = df_partidos.iloc[0]
        
        st.subheader(f"Partido #{partido['id']}")
        col1, col2, col3 = st.columns([2,1,2])
        with col1: st.write(f"**{partido['equipo_local']}**")
        with col2: gl = st.number_input("Goles L", min_value=0, step=1, key="gl")
        with col3: st.write(f"**{partido['equipo_visitante']}**")
        
        gv = st.number_input(f"Goles {partido['equipo_visitante']}", min_value=0, step=1, key="gv")

        # GENERAR LINK MÁGICO
        # Usamos los mismos entry.XXXX que ya verificamos
        params = {
            "entry.331238612": usuario,
            "entry.1706692557": str(partido['id']),
            "entry.1741549419": str(gl),
            "entry.1351187424": str(gv)
        }
        
        query_string = urllib.parse.urlencode(params)
        final_link = f"{BASE_FORM_URL}?{query_string}"

        st.write("---")
        st.markdown(f"""
            <a href="{final_link}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#00cc44;color:white;padding:15px;border-radius:10px;text-align:center;font-weight:bold;font-size:20px;">
                    ✅ TOCÁ ACÁ PARA GUARDAR EN EXCEL
                </div>
            </a>
        """, unsafe_url=True)
        st.caption("Se abrirá una ventana de Google Forms con los datos ya listos, solo dale a 'Enviar'.")

except Exception as e:
    st.error(f"Error: {e}")
