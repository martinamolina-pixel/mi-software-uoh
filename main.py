import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Configuración base
st.set_page_config(page_title="Software Clínico EsSa-UOH", layout="wide")

st.title("🏥 REGISTRO CLÍNICO")
st.subheader("EVALUACIÓN INTERNADO APS")

# 2. Formulario Simplificado para evitar errores
with st.container():
    st.info("📌 DATOS DEL PACIENTE")
    col1, col2 = st.columns(2)
    with col1:
        nombre_paciente = st.text_input("Nombre Paciente")
        edad = st.text_input("Edad")
    with col2:
        interno = st.text_input("Nombre Interno")
        diag_nutricional = st.text_input("Diagnóstico Nutricional")

# 3. Botón de Guardado
if st.button("💾 GUARDAR REGISTRO CLÍNICO"):
    if nombre_paciente == "":
        st.error("Escribe el nombre del paciente antes de guardar.")
    else:
        try:
            # Conexión
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # Datos a enviar
            nuevo_registro = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Paciente": nombre_paciente,
                "Edad": edad,
                "Interno": interno,
                "Diagnostico": diag_nutricional
            }])

            # GUARDAR (Usaremos el nombre por defecto para no fallar)
            conn.create(data=nuevo_registro)
            
            st.balloons()
            st.success(f"¡Felicidades Martina! El registro de {nombre_paciente} se guardó.")
        except Exception as e:
            st.error(f"Error de conexión. Revisa los Secrets. Detalles: {e}")
