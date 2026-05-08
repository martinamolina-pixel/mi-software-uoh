import streamlit as st
from fpdf import FPDF
from datetime import datetime

# 1. Configuración inicial y Logo
st.set_page_config(page_title="Registro Clínico UOH", page_icon="🏥", layout="centered")

# Mostramos el logo de la Universidad/Escuela al principio
st.image("https://www.uoh.cl/vinculacion/wp-content/uploads/2022/10/Logo-UOH-Escuela-de-Salud-01.png", width=350)
st.title("REGISTRO CLÍNICO INTERNADO APS")
st.write("---")

# --- CLASE PDF CON LOGO ---
class PDF(FPDF):
    def header(self):
        # Logo en el PDF
        try:
            logo_url = "https://drive.google.com/uc?id=1im706wttlyX4vA5v_gWcmBAg5KRSbH6r"
            self.image(logo_url, 10, 8, 33)
        except:
            self.set_font('Arial', 'B', 10)
            self.cell(0, 10, 'UNIVERSIDAD DE O\'HIGGINS - ESCUELA DE SALUD', 0, 1, 'L')
        
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'FICHA DE EVALUACIÓN TEÓRICO PRÁCTICA', 0, 1, 'C')
        self.ln(10)

# --- INTERFAZ DEL SOFTWARE ---
with st.form("registro_completo"):
    # Organizamos por secciones para que sea fácil en la tablet
    st.subheader("I. IDENTIFICACIÓN")
    col1, col2 = st.columns(2)
    nombre = col1.text_input("Nombre Paciente")
    edad = col2.text_input("Edad")
    domicilio = st.text_input("Domicilio")
    interno = st.text_input("Nombre Interno(a) de Enfermería")

    st.subheader("II. ENTREVISTA Y ALIMENTACIÓN")
    tipo_alim = st.radio("Tipo de Alimentación", ["LME", "LA", "LM+LA", "COMPLEMENTARIA"], horizontal=True)
    obs_alim = st.text_area("Observaciones Alimentación")
    
    st.subheader("III. CLÍNICA")
    meds = st.text_area("Medicamentos / Suplementos")
    examenes = st.text_area("Vacunas / Exámenes / Radiografías")
    instrumentos = st.text_area("Instrumentos / Resultados (EEDP, Score, etc.)")

    st.subheader("IV. ANTROPOMETRÍA")
    c1, c2, c3 = st.columns(3)
    peso = c1.text_input("Peso")
    talla = c2.text_input("Talla")
    pc = c3.text_input("Perímetro Craneano")
    pe = c1.text_input("P/E")
    te = c2.text_input("T/E")
    pt = c3.text_input("P/T")
    diag_nutri = st.text_area("Diagnóstico Nutricional")

    st.subheader("V. PLAN DE CIERRE")
    indicaciones = st.text_area("Acuerdos e Indicaciones")
    derivaciones = st.text_area("Derivaciones")

    boton_final = st.form_submit_button("✨ GENERAR REGISTRO PDF")

# --- LÓGICA DE GENERACIÓN ---
if boton_final:
    if not nombre:
        st.warning("Por favor, ingresa el nombre del paciente.")
    else:
        try:
            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", "", 11)
            
            # Formato de celdas para el PDF
            def agregar_seccion(pdf, titulo, contenido):
                pdf.set_font("Arial", "B", 11)
                pdf.set_fill_color(240, 240, 240)
                pdf.cell(0, 8, titulo, 1, 1, 'L', fill=True)
                pdf.set_font("Arial", "", 10)
                pdf.multi_cell(0, 7, contenido, 1)
                pdf.ln(3)

            # Llenar secciones
            agregar_seccion(pdf, "I. IDENTIFICACIÓN", f"Paciente: {nombre}\nEdad: {edad}\nDomicilio: {domicilio}\nInterno: {interno}")
            agregar_seccion(pdf, "II. ENTREVISTA", f"Alimentación: {tipo_alim}\nObs: {obs_alim}")
            agregar_seccion(pdf, "III. MEDICAMENTOS Y EXÁMENES", f"Meds: {meds}\nExámenes/Vacunas: {examenes}\nInst: {instrumentos}")
            agregar_seccion(pdf, "IV. ANTROPOMETRÍA", f"P: {peso} | T: {talla} | PC: {pc}\nP/E: {pe} | T/E: {te} | P/T: {pt}\nDiag: {diag_nutri}")
            agregar_seccion(pdf, "V. PLAN Y DERIVACIONES", f"Indicaciones: {indicaciones}\nDerivaciones: {derivaciones}")

            pdf_bytes = pdf.output()
            
            st.success("¡Registro completado con éxito!")
            st.download_button(
                label="📥 DESCARGAR REGISTRO PDF",
                data=bytes(pdf_bytes),
                file_name=f"Registro_{nombre.replace(' ','_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar el documento: {e}")
