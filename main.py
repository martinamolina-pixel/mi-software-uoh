import streamlit as st
from fpdf import FPDF
import base64

# 1. Configuración de página y Estética
st.set_page_config(page_title="Registro Clínico UOH", page_icon="🏥", layout="centered")

# --- FUNCIÓN PARA EL LOGO (SOLUCIÓN INFALIBLE) ---
# Si la URL falla, el sistema no se cae y usa el nombre institucional
LOGO_URL = "https://raw.githubusercontent.com/UOH-Salud/logos/main/escuela_salud.png" 

def mostrar_logo():
    try:
        # Intentamos cargar desde el link directo de Drive corregido
        st.image("https://drive.google.com/uc?id=1QD40i4hMpGqGxpx7Zaw8JLad3CwPHo_x", width=300)
    except:
        st.header("🏥 ESCUELA DE SALUD - UOH")

mostrar_logo()
st.title("Sistema de Registro Clínico")

# --- CLASE PARA EL REPORTE PDF ---
class PDF(FPDF):
    def header(self):
        try:
            # Logo en PDF (mismo link directo)
            self.image("https://drive.google.com/uc?id=1QD40i4hMpGqGxpx7Zaw8JLad3CwPHo_x", 10, 8, 33)
        except:
            self.set_font('Arial', 'B', 10)
            self.cell(0, 10, 'UNIVERSIDAD DE O\'HIGGINS', 0, 1, 'L')
        
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'FICHA CLÍNICA DE ATENCIÓN APS', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Créditos solicitados en el informe
        self.cell(0, 10, 'Sistema generado por el Centro de Habilidades Clínicas y Disciplinares - UOH', 0, 0, 'C')

# --- INTERFAZ POR SEGMENTOS (TABS) ---
with st.form("software_registro"):
    # Volvemos a las pestañas que pediste
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Identificación", "🩺 Clínica", "📊 Antropometría", "📝 Cierre"])

    with tab1:
        nombre = st.text_input("Nombre del Paciente")
        c1, c2 = st.columns(2)
        edad = c1.text_input("Edad")
        domicilio = c2.text_input("Domicilio")
        interno = st.text_input("Interno(a) de Enfermería Responsable")

    with tab2:
        st.info("Detalles de la atención actual")
        tipo_alim = st.selectbox("Tipo Alimentación", ["LME", "LA", "LM+LA", "Complementaria"])
        obs_alim = st.text_area("Observaciones de Alimentación")
        meds = st.text_area("Medicamentos / Suplementos")
        examenes = st.text_area("Vacunas / Exámenes Vigentes")

    with tab3:
        st.write("### Evaluación Nutricional")
        col_a, col_b, col_c = st.columns(3)
        peso = col_a.text_input("Peso (kg)")
        talla = col_b.text_input("Talla (cm)")
        pc = col_c.text_input("P. Craneano")
        pe = col_a.text_input("P/E")
        te = col_b.text_input("T/E")
        pt = col_c.text_input("P/T")
        diag = st.text_area("Diagnóstico Nutricional Integrado")

    with tab4:
        indicaciones = st.text_area("Acuerdos e Indicaciones para el paciente")
        derivaciones = st.text_area("Derivaciones / Interconsultas")

    # Botón de acción
    enviar = st.form_submit_button("🚀 GENERAR REGISTRO CLÍNICO")

# --- GENERACIÓN DEL DOCUMENTO ---
if enviar:
    if not nombre:
        st.error("⚠️ Por favor ingresa el nombre del paciente.")
    else:
        try:
            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=11)
            
            # Bloques de datos
            def add_section(title, text):
                pdf.set_font("Arial", 'B', 11)
                pdf.set_fill_color(230, 230, 230)
                pdf.cell(0, 8, title, 1, 1, 'L', fill=True)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 7, text, 1)
                pdf.ln(4)

            add_section("I. IDENTIFICACIÓN", f"Paciente: {nombre}\nEdad: {edad}\nInterno: {interno}\nDomicilio: {domicilio}")
            add_section("II. DATOS CLÍNICOS", f"Alimentación: {tipo_alim}\nObs: {obs_alim}\nMedicamentos: {meds}\nExámenes: {examenes}")
            add_section("III. ANTROPOMETRÍA", f"Peso: {peso} | Talla: {talla} | PC: {pc}\nIndicadores: P/E:{pe}, T/E:{te}, P/T:{pt}\nDiagnóstico: {diag}")
            add_section("IV. CIERRE", f"Indicaciones: {indicaciones}\nDerivaciones: {derivaciones}")

            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            st.success("✅ ¡Ficha generada con éxito!")
            st.download_button(
                label="📥 DESCARGAR INFORME EN PDF",
                data=pdf_output,
                file_name=f"Ficha_{nombre.replace(' ','_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Hubo un error al crear el PDF: {e}")

# --- CRÉDITOS INSTITUCIONALES (FOOTER APP) ---
st.write("---")
st.caption("Sistema generado por el Centro de Habilidades Clínicas y Disciplinares - Universidad de O'Higgins")
