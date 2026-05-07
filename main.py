import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Configuración básica
st.set_page_config(page_title="Software Clínico EsSa-UOH", layout="wide")

st.title("🏥 REGISTRO CLÍNICO")
st.subheader("EVALUACIÓN INTERNADO APS")

# 2. Formulario
with st.container():
    st.info("📌 IDENTIFICACIÓN")
    nombre_paciente = st.text_input("Nombre Paciente")
    edad = st.text_input("Edad")
    interno = st.text_input("Nombre Interno")
    diag = st.text_input("Diagnóstico Nutricional")

# 3. Botón de Guardado
if st.button("💾 GUARDAR REGISTRO CLÍNICO"):
    if not nombre_paciente:
        st.warning("Escribe el nombre del paciente.")
    else:
        try:
            # Conexión mágica
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # Formatear datos
            df_nuevo = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%d/%m/%Y"),
                "Paciente": nombre_paciente,
                "Edad": edad,
                "Interno": interno,
                "Diagnostico": diag
            }])

            # GUARDAR
            # Importante: Esto guardará en la primera hoja que encuentre
            conn.create(data=df_nuevo)
            
            st.balloons()
            st.success(f"¡LOGRADO! El registro de {nombre_paciente} ya está en tu Excel.")
        except Exception as e:
            st.error(f"Hay un problema con la conexión a Google: {e}")
