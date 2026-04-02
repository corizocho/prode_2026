import streamlit as st
import pandas as pd
import urllib.parse

# --- CONFIGURACIÓN ---
# Tu ID de Sheet y el link base del Formulario
SHEET_ID = "1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10"
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
        st.info("Cargá tus goles y usá el botón verde para guardar.")
        
        # Tomamos el primer partido para la prueba
        partido = df_partidos.iloc[0]
        
        st.subheader(f"Partido #{partido['id']}")
        
        # Diseño en una sola fila para que no se rompa el tablero
        c1, c2, c3, c4, c5 = st.columns([2, 1, 0.5, 1, 2])
        
        with c1: st.write(f"**{partido['equipo_local']}**")
        with c2: gl = st.number_input("L", min_value=0, step=1, key="gl", label_visibility="collapsed")
        with c3: st.write("vs")
        with c4: gv = st.number_input("V", min_value=0, step=1, key="gv", label_visibility="collapsed")
        with c5: st.write(f"**{partido['equipo_visitante']}**")

        # GENERAR LINK MÁGICO
        params = {
            "entry.331238612": usuario,
            "entry.1706692557": str(partido['id']),
            "entry.1741549419": str(gl),
            "entry.1351187424": str(gv)
        }
        
        query_string = urllib.parse.urlencode(params)
        final_link = f"{BASE_FORM_URL}?{query_string}"

        st.write("---")
        # ACÁ ESTÁ EL ARREGLO: 'unsafe_allow_html' en lugar de 'unsafe_url'
        st.markdown(f"""
            <a href="{final_link}" target="_blank" style="text-decoration:none;">
                <div style="background-color:#00cc44;color:white;padding:15px;border-radius:10px;text-align:center;font-weight:bold;font-size:20px;">
                    ✅ GUARDAR RESULTADO
                </div>
            </a>
        """, unsafe_allow_html=True)
        
        st.caption("Al tocar se abrirá el formulario con los datos listos. Solo dale a 'Enviar'.")

except Exception as e:
    st.error(f"Error al cargar: {e}")
