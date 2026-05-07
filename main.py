import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Software Clínico EsSa-UOH", layout="wide")

# Estilos para que parezca una ficha médica
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1, h2 { color: #004a99; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #e1e8f0;
        border-radius: 4px 4px 0px 0px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 REGISTRO CLÍNICO")
st.subheader("EVALUACIÓN TEÓRICA PRÁCTICA FINAL - INTERNADO APS")

# --- FORMULARIO ---
with st.container():
    # 1. DATOS IDENTIFICACIÓN
    st.info("📌 IDENTIFICACIÓN")
    col1, col2 = st.columns(2)
    with col1:
        nombre_paciente = st.text_input("Nombre Paciente")
        edad = st.text_input("Edad")
    with col2:
        domicilio = st.text_input("Domicilio")
        interno = st.text_input("Nombre Interno Enfermería")

    # 2. ENTREVISTA Y ALIMENTACIÓN
    st.info("🎙️ ENTREVISTA")
    tipo_alimentacion = st.selectbox("TIPO ALIMENTACIÓN", ["LME", "LA", "LM+LA", "COMPLEMENTARIA"])
    obs_entrevista = st.text_area("Observaciones Entrevista")

    # 3. TRATAMIENTO Y PREVENCIÓN
    st.info("💊 MEDICAMENTOS Y PREVENCIÓN")
    col3, col4 = st.columns(2)
    with col3:
        medicamentos = st.text_area("MEDICAMENTOS/SUPLEMENTOS")
    with col4:
        vacunas = st.text_area("VACUNAS/ EXÁMENES /RADIOGRAFÍAS")

    # 4. RESULTADOS E INSTRUMENTOS
    st.info("📊 INSTRUMENTOS")
    instrumentos = st.text_area("INSTRUMENTOS/RESULTADOS")

    # 5. ANTROPOMETRÍA (Aquí el software calcula solo)
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

    # 6. CIERRE
    st.info("📝 ACUERDOS Y DERIVACIONES")
    col5, col6 = st.columns(2)
    with col5:
        indicaciones = st.text_area("ACUERDOS E INDICACIONES")
    with col6:
        derivaciones = st.text_area("DERIVACIONES")

# Botón para finalizar
if st.button("💾 GUARDAR REGISTRO CLÍNICO"):
    st.balloons()
    st.success(f"Registro de {nombre_paciente} completado con éxito.")
