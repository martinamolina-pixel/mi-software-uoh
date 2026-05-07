import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración básica
st.set_page_config(page_title="Ficha Clínica UOH", layout="centered")

st.title("🏥 REGISTRO CLÍNICO")
st.write("Internado APS - Martina Molina")

# Formulario ultra-seguro
with st.form("ficha_medica"):
    nombre = st.text_input("Nombre Paciente")
    edad = st.text_input("Edad")
    diag = st.text_input("Diagnóstico")
    enviar = st.form_submit_button("💾 GUARDAR EN EXCEL")

if enviar:
    if not nombre:
        st.warning("Escribe el nombre.")
    else:
        try:
            # Conexión directa
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # Crear la fila
            df = pd.DataFrame([{"Paciente": nombre, "Edad": edad, "Diagnostico": diag}])
            
            # Guardar
            conn.create(data=df)
            
            st.balloons()
            st.success(f"¡LOGRADO! Datos de {nombre} guardados.")
        except Exception as e:
            st.error(f"Error: {e}")
