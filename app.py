import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")
ID_SHEET = "1BACdwjatwM85mpPkSAOXY8l3IP-MecfjgYqa7USZw10"

def conectar_google():
    try:
        # Cargamos los secretos
        s = st.secrets["gcp_service_account"]
        
        # Limpieza extrema de la private_key
        # Esto quita comillas extra, espacios al inicio/final y arregla los saltos de línea
        pk = s["private_key"].replace("\\n", "\n").strip()
        if pk.startswith('"') and pk.endswith('"'):
            pk = pk[1:-1]

        info = {
            "type": s["type"],
            "project_id": s["project_id"],
            "private_key_id": s["private_key_id"],
            "private_key": pk,
            "client_email": s["client_email"],
            "client_id": s["client_id"],
            "auth_uri": s["auth_uri"],
            "token_uri": s["token_uri"],
            "auth_provider_x509_cert_url": s["auth_provider_x509_cert_url"],
            "client_x509_cert_url": s["client_x509_cert_url"]
        }
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(info, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error al procesar la llave: {e}")
        st.stop()

# --- INICIO DE LA APP ---
try:
    client = conectar_google()
    spreadsheet = client.open_by_key(ID_SHEET)
    
    st.title("🏆 PRODE MUNDIAL 2026")
    t1, t2 = st.tabs(["⚽ Cargar Goles", "📊 Posiciones"])

    with t1:
        st.header("Cargá tu pronóstico")
        nombre = st.text_input("Tu Nombre:")
        
        ws_p = spreadsheet.worksheet("Partidos")
        df_p = pd.DataFrame(ws_p.get_all_records())
        
        opciones = df_p['equipo_local'] + " vs " + df_p['equipo_visitante']
        sel = st.selectbox("Seleccioná el partido:", opciones)
        id_partido = df_p.iloc[opciones.tolist().index(sel)]['id']
        
        c1, c2 = st.columns(2)
        g_l = c1.number_input("Goles Local", min_value=0, step=1, key="l")
        g_v = c2.number_input("Goles Vis", min_value=0, step=1, key="v")
        
        if st.button("Enviar Pronóstico"):
            if nombre:
                ws_res = spreadsheet.worksheet("Respuestas de formulario 1")
                # Formato exacto para que el Excel lo entienda como fecha/hora
                ahora = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')
                ws_res.append_row([ahora, nombre, id_partido, g_l, g_v])
                st.success(f"✅ ¡Guardado, {nombre}!")
                st.balloons()
            else:
                st.warning("Escribí tu nombre.")

    with t2:
        st.header("🏆 Tabla de Posiciones")
        try:
            ws_rank = spreadsheet.worksheet("CalculoPuntos")
            df_r = pd.DataFrame(ws_rank.get_all_records())
            
            # Filtramos filas vacías
            df_r = df_r[df_r['Usuario'] != ""]
            
            # Sumamos puntos por usuario
            res = df_r.groupby("Usuario")["Puntos"].sum().reset_index()
            res = res.sort_values("Puntos", ascending=False).reset_index(drop=True)
            
            st.table(res)
            
            if not res.empty:
                st.info(f"🥇 Puntero actual: **{res.iloc[0]['Usuario']}**")
        except:
            st.info("No hay datos de puntos todavía.")

except Exception as e:
    st.error("Error de conexión.")
    st.write(f"Detalle técnico: {e}")
    st.info("💡 Si el error persiste, reiniciá la app desde el panel de Streamlit (Reboot App).")
