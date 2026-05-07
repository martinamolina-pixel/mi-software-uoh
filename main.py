import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Registro Clínico APS UOH", layout="centered")

# --- FUNCIÓN PARA GENERAR EL PDF ---
class PDF(FPDF):
    def header(self):
        # Logo institucional (Si el link de Drive no carga, el PDF seguirá funcionando)
        try:
            # Reemplazamos el link de vista por el de descarga directa
            logo_url = "https://drive.google.com/uc?id=1im706wttlyX4vA5v_gWcmBAg5KRSbH6r"
            self.image(logo_url, 10, 8, 33)
        except:
            self.set_font('Arial', 'B', 8)
            self.cell(0, 10, 'LOGO UOH', 0, 0, 'L')
            
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'REGISTRO CLÍNICO - INTERNADO APS', ln=True, align='C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Evaluación Teórica Práctica Final', ln=True, align='C')
        self.ln(10)

def generar_pdf_integral(datos):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 11)
    
    # SECCIÓN 1: IDENTIFICACIÓN
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "1. IDENTIFICACIÓN DEL PACIENTE", 1, ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Paciente: {datos['nombre']} | Edad: {datos['edad']}", 1, ln=True)
    pdf.cell(0, 8, f"Domicilio: {datos['domicilio']}", 1, ln=True)
    pdf.cell(0, 8, f"Interno(a) Responsable: {datos['interno']}", 1, ln=True)
    pdf.ln(5)

    # SECCIÓN 2: ENTREVISTA Y ALIMENTACIÓN
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "2. ENTREVISTA Y ALIMENTACIÓN", 1, ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Tipo de Alimentación: {datos['tipo_alim']}", 1, ln=True)
    pdf.multi_cell(0, 8, f"Observaciones Alimentación: {datos['obs_alim']}", 1)
    pdf.ln(5)

    # SECCIÓN 3: HISTORIA CLÍNICA
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "3. MEDICAMENTOS, EXÁMENES E INSTRUMENTOS", 1, ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, f"Medicamentos/Suplementos: {datos['meds']}", 1)
    pdf.multi_cell(0, 8, f"Vacunas/Exámenes/Radiografías: {datos['examenes']}", 1)
    pdf.multi_cell(0, 8, f"Instrumentos/Resultados: {datos['instrumentos']}", 1)
    pdf.ln(5)

    # SECCIÓN 4: ANTROPOMETRÍA
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "4. ANTROPOMETRÍA Y DIAGNÓSTICO", 1, ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(60, 8, f"Peso: {datos['peso']}", 1)
    pdf.cell(60, 8, f"Talla: {datos['talla']}", 1)
    pdf.cell(0, 8, f"P. Craneano: {datos['pc']}", 1, ln=True)
    pdf.cell(60, 8, f"P/E: {datos['pe']}", 1)
    pdf.cell(60, 8, f"T/E: {datos['te']}", 1)
    pdf.cell(0, 8, f"P/T: {datos['pt']}", 1, ln=True)
    pdf.multi_cell(0, 8, f"Diagnóstico Nutricional: {datos['diag_nutri']}", 1)
    pdf.ln(5)

    # SECCIÓN 5: INDICACIONES
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 8, "5. ACUERDOS, INDICACIONES Y DERIVACIONES", 1, ln=True, fill=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, f"Acuerdos e Indicaciones: {datos['indicaciones']}", 1)
    pdf.multi_cell(0, 8, f"Derivaciones: {datos['derivaciones']}", 1)

    return pdf.output()

# --- INTERFAZ DE STREAMLIT ---
st.title("🏥 Sistema de Registro Clínico APS")
st.subheader("Internado Enfermería UOH")

with st.form("registro_integral"):
    # Usamos pestañas para organizar la gran cantidad de datos
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Identificación", "🥗 Entrevista", "📏 Antropometría", "📝 Plan"])

    with tab1:
        nombre = st.text_input("Nombre del Paciente")
        col_id1, col_id2 = st.columns(2)
        edad = col_id1.text_input("Edad")
        domicilio = col_id2.text_input("Domicilio")
        interno = st.text_input("Nombre Interno(a) de Enfermería")

    with tab2:
        tipo_alim = st.selectbox("Tipo de Alimentación", ["LME", "LA", "LM+LA", "Complementaria"])
        obs_alim = st.text_area("Observaciones Alimentación")
        meds = st.text_area("Medicamentos/Suplementos")
        examenes = st.text_area("Vacunas / Exámenes / Radiografías")
        instrumentos = st.text_area("Instrumentos / Resultados (EEDP, Score, etc)")

    with tab3:
        col_an1, col_an2, col_an3 = st.columns(3)
        peso = col_an1.text_input("Peso (kg)")
        talla = col_an2.text_input("Talla (cm)")
        pc = col_an3.text_input("P. Craneano")
        
        col_an4, col_an5, col_an6 = st.columns(3)
        pe = col_an4.text_input("P/E")
        te = col_an5.text_input("T/E")
        pt = col_an6.text_input("P/T")
        
        diag_nutri = st.text_area("Diagnóstico Nutricional")

    with tab4:
        indicaciones = st.text_area("Acuerdos e Indicaciones")
        derivaciones = st.text_area("Derivaciones")
        
    submit = st.form_submit_button("✨ GENERAR REGISTRO COMPLETO PDF")

if submit:
    if not nombre:
        st.error("Falta el nombre del paciente.")
    else:
        datos_completos = {
            "nombre": nombre, "edad": edad, "domicilio": domicilio, "interno": interno,
            "tipo_alim": tipo_alim, "obs_alim": obs_alim, "meds": meds,
            "examenes": examenes, "instrumentos": instrumentos,
            "peso": peso, "talla": talla, "pc": pc, "pe": pe, "te": te, "pt": pt,
            "diag_nutri": diag_nutri, "indicaciones": indicaciones, "derivaciones": derivaciones
        }
        
        try:
            pdf_result = generar_pdf_integral(datos_completos)
            st.success("✅ Registro Clínico generado con éxito.")
            st.download_button(
                label="📥 DESCARGAR FICHA CLÍNICA PDF",
                data=bytes(pdf_result),
                file_name=f"Registro_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar PDF: {e}")
