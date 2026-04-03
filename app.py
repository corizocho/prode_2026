import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Prode Mundial 2026", layout="centered")
ID_SHEET = "1BACdwjatWM8mpPKSAOXY8I3IP-MecfJgyqa7OSZWTO"

def conectar_google():
    try:
        # Traemos la info de los Secrets
        secret_info = st.secrets["gcp_service_account"]
        
        # LIMPIEZA CRÍTICA: Esto arregla la llave si tiene errores de formato
        # Reemplaza los saltos de línea literales por los que entiende Python
        limpiar_llave = secret_info["private_key"].replace("\\n", "\n")
        
        # Armamos el diccionario de credenciales nuevo
        creds_dict = {
            "type": secret_info["type"],
            "project_id": secret_info["project_id"],
            "private_key_id": secret_info["private_key_id"],
            "private_key": limpiar_llave,
            "client_email": secret_info["client_email"],
            "client_id": secret_info["client_id"],
            "auth_uri": secret_info["auth_uri"],
            "token_uri": secret_info["token_uri"],
            "auth_provider_x509_cert_url": secret_info["auth_provider_x509_cert_url"],
            "client_x509_cert_url": secret_info["client_x509_cert_url"]
        }
        
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Error detectado en los Secrets: {e}")
        st.stop()

# --- INICIO DE LA APLICACIÓN ---
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
        sel = st.selectbox("Partido:", opciones)
        id_partido = df_p.iloc[opciones.tolist().index(sel)]['id']
        
        c1, c2 = st.columns(2)
        g_l = c1.number_input("Goles Local", min_value=0, step=1, key="l")
        g_v = c2.number_input("Goles Vis", min_value=0, step=1, key="v")
        
        if st.button("Enviar"):
            if nombre:
                ws_res = spreadsheet.worksheet("Respuestas de formulario 1")
                ws_res.append_row([pd.Timestamp.now().strftime('%d/%m/%Y %H:%M'), nombre, id_partido, g_l, g_v])
                st.success("✅ ¡Guardado! Ya podés cerrar.")
                st.balloons()
            else:
                st.warning("Escribí tu nombre.")

    with t2:
        st.header("🏆 Posiciones")
        try:
            ws_rank = spreadsheet.worksheet("CalculoPuntos")
            df_r = pd.DataFrame(ws_rank.get_all_records())
            # Filtramos por si hay filas vacías
            df_r = df_r[df_r['Usuario'] != ""]
            res = df_r.groupby("Usuario")["Puntos"].sum().reset_index()
            st.table(res.sort_values("Puntos", ascending=False).reset_index(drop=True))
        except:
            st.info("Cargando ranking...")

except Exception as e:
    st.error("Error de conexión final.")
    st.write(f"Detalle: {e}")
