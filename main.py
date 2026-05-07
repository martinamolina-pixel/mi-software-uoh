import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Software Clínico EsSa-UOH", layout="wide")

# Estilos médicos
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1, h2 { color: #004a99; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 REGISTRO CLÍNICO")
st.subheader("EVALUACIÓN TEÓRICA PRÁCTICA FINAL - INTERNADO APS")

# --- FORMULARIO ---
with st.container():
    st.info("📌 IDENTIFICACIÓN")
    col1, col2 = st.columns(2)
    with col1:
        nombre_paciente = st.text_input("Nombre Paciente")
        edad = st.text_input("Edad")
    with col2:
        domicilio = st.text_input("Domicilio")
        interno = st.text_input("Nombre Interno Enfermería")

    st.info("🎙️ ENTREVISTA")
    tipo_alimentacion = st.selectbox("TIPO ALIMENTACIÓN", ["LME", "LA", "LM+LA", "COMPLEMENTARIA"])
    obs_entrevista = st.text_area("Observaciones Entrevista")

    st.info("💊 MEDICAMENTOS Y PREVENCIÓN")
    col3, col4 = st.columns(2)
    with col3:
        medicamentos = st.text_area("MEDICAMENTOS/SUPLEMENTOS")
    with col4:
        vacunas = st.text_area("VACUNAS/ EXÁMENES /RADIOGRAFÍAS")

    st.info("📊 INSTRUMENTOS")
    instrumentos = st.text_area("INSTRUMENTOS/RESULTADOS")

    st.info("📏 ANTROPOMETRÍA")
    c1, c2, c3 = st.columns(3)
    with c1:
        peso = st.number_input("Peso (kg)", min_value=0.0, step=0.1)
        pe = st.text_input("P/E (Peso/Edad)")
    with c2:
        talla = st.number_input("Talla (cm)", min_value=0.0, step=0.1)
        te = st.text_input("T/E (Talla/Edad)")
    with c3:
        p_craneano = st.number_input("Perímetro Craneano (cm)", min_value=0.0, step=0.1)
        pt = st.text_input("P/T (Peso/Talla)")
    
    diag_nutricional = st.text_input("Diagnóstico Nutricional")

    st.info("📝 ACUERDOS Y DERIVACIONES")
    col5, col6 = st.columns(2)
    with col5:
        indicaciones = st.text_area("ACUERDOS E INDICACIONES")
    with col6:
        derivaciones = st.text_area("DERIVACIONES")

# --- LÓGICA DE GUARDADO REAL ---
if st.button("💾 GUARDAR REGISTRO CLÍNICO"):
    if nombre_paciente == "":
        st.error("Por favor, ingresa al menos el nombre del paciente.")
    else:
        try:
            # Crear conexión
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # Preparar los datos para enviar
            nuevo_registro = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Paciente": nombre_paciente,
                "Edad": edad,
                "Interno": interno,
                "Domicilio": domicilio,
                "Alimentacion": tipo_alimentacion,
                "Peso": peso,
                "Talla": talla,
                "Diagnostico": diag_nutricional,
                "Indicaciones": indicaciones
            }])

            # ENVIAR A GOOGLE SHEETS
            # (Asegúrate que tu hoja se llame "Hoja 1" o cambia el nombre aquí)
            existentes = conn.read(worksheet="Hoja 1")
            actualizados = pd.concat([existentes, nuevo_registro], ignore_index=True)
            conn.update(worksheet="Hoja 1", data=actualizados)

            st.balloons()
            st.success(f"¡Registro de {nombre_paciente} guardado en Google Sheets con éxito!")
        except Exception as e:
            st.error(f"Error al conectar con Google Sheets: {e}")
