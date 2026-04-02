import streamlit as st
import pandas as pd
import urllib.parse

# --- CONFIGURACIÓN ---
SHEET_ID = "1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10"
# Link base con el parámetro de pre-rellenado
BASE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe-N62t_1nQAK08u0Orr23Zk5fu69vo34chTa229CCiQx5mQA/viewform?usp=pp_url"

st.set_page_config(page_title="Prode 2026", page_icon="⚽")
st.title("🏆 Mi Prode 2026")

# --- CARGA DE DATOS ---
url_partidos = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Partidos"

try:
    df_partidos = pd.read_csv(url_partidos)
    nombres = ["Juan", "Pedro", "Maria", "Corizocho", "nicolas", "edu"] 
    usuario = st.sidebar.selectbox("¿Quién sos?", ["Seleccionar..."] + nombres)

    if usuario != "Seleccionar...":
        st.header(f"Hola {usuario}")
        st.info("Cargá tus goles y usá el botón verde para enviar al Excel.")
        
        # Iteramos por todos los partidos que tengas en la pestaña 'Partidos'
        for index, row in df_partidos.iterrows():
            st.subheader(f"Partido #{row['id']}")
            
            c1, c2, c3, c4, c5 = st.columns([2, 1, 0.5, 1, 2])
            with c1: st.write(f"**{row['equipo_local']}**")
            with c2: gl = st.number_input("L", min_value=0, step=1, key=f"l_{row['id']}", label_visibility="collapsed")
            with c3: st.write("vs")
            with c4: gv = st.number_input("V", min_value=0, step=1, key=f"v_{row['id']}", label_visibility="collapsed")
            with c5: st.write(f"**{row['equipo_visitante']}**")

            # GENERAR LINK MÁGICO CON TUS NUEVOS IDs
            params = {
                "entry.1805862975": usuario,
                "entry.443574248": str(row['id']),
                "entry.632622784": str(gl),
                "entry.1062890017": str(gv)
            }
            
            query_string = urllib.parse.urlencode(params)
            final_link = f"{BASE_FORM_URL}&{query_string}"

            st.markdown(f"""
                <a href="{final_link}" target="_blank" style="text-decoration:none;">
                    <div style="background-color:#00cc44;color:white;padding:10px;border-radius:8px;text-align:center;font-weight:bold;">
                        ✅ GUARDAR RESULTADO {row['equipo_local']} vs {row['equipo_visitante']}
                    </div>
                </a>
            """, unsafe_allow_html=True)
            st.write("---")

except Exception as e:
    st.error(f"Error: {e}")
