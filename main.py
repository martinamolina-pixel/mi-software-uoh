import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# 1. CONFIGURACIÓN ESTÉTICA
st.set_page_config(page_title="Registro Clínico UOH", page_icon="🏥", layout="centered")

# CSS Personalizado para un look más moderno y limpio
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    h1 { color: #003366; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-weight: 800; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        padding: 12px 25px;
        font-weight: 600;
        color: #003366;
    }
    .stTabs [aria-selected="true"] {
        background-color: #003366 !important;
        color: white !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .footer-uoh {
        text-align: center;
        color: #475569;
        font-size: 0.85rem;
        border-top: 2px solid #003366;
        padding-top: 20px;
        margin-top: 60px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
NOMBRE_LOGO = "UOH - EsSa Azul (1) (3) (1).png"

if os.path.exists(NOMBRE_LOGO):
    st.image(NOMBRE_LOGO, width=420)
else:
    st.title("🏥 SISTEMA DE REGISTRO CLÍNICO")

st.markdown("<h4 style='color: #64748b; margin-top:-20px;'>Escuela de Salud | Unidad de Internado</h4>", unsafe_allow_html=True)
st.write("---")

# --- CLASE PDF PROFESIONAL ---
class ReporteClinico(FPDF):
    def header(self):
        if os.path.exists(NOMBRE_LOGO):
            self.image(NOMBRE_LOGO, 10, 8, 35)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'INFORME DE EVALUACIÓN CLÍNICA APS', 0, 1, 'R')
        self.set_draw_color(0, 51, 102)
        self.line(10, 26, 200, 26)
        self.ln(12)

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 116, 139)
        self.line(10, 275, 200, 275)
        self.cell(0, 10, 'Centro de Habilidades Clínicas y Disciplinares - UOH', 0, 0, 'L')
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'R')

def crear_pdf(datos):
    pdf = ReporteClinico()
    pdf.add_page()
    
    def sec(titulo, texto):
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(235, 241, 250)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 9, f" {titulo}", 1, 1, 'L', fill=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(30, 41, 59)
        pdf.multi_cell(0, 7, str(texto), 1)
        pdf.ln(4)

    sec("I. IDENTIFICACIÓN", f"Paciente: {datos['nombre']}\nEdad: {datos['edad']}\nDomicilio: {datos['domicilio']}\nInterno: {datos['interno']}")
    sec("II. ENTREVISTA GENERAL", datos['entrevista'])
    sec("III. VALORACIÓN CLÍNICA Y ALIMENTACIÓN", f"Alimentación: {datos['tipo_alim']}\nDetalles: {datos['obs_alim']}\nMeds: {datos['meds']}\nExámenes/Vacunas: {datos['examenes']}")
    sec("IV. ANTROPOMETRÍA", f"P: {datos['peso']} kg | T: {datos['talla']} cm | PC: {datos['pc']} cm\nP/E: {datos['pe']} | T/E: {datos['te']} | P/T: {datos['pt']}\nDiagnóstico: {datos['diag']}")
    sec("V. ACUERDOS Y DERIVACIONES", f"Indicaciones: {datos['ind']}\nDerivaciones: {datos['der']}")
    
    return pdf.output(dest='S')

# --- FORMULARIO POR PESTAÑAS ---
with st.form("registro_maestro_uoh"):
    # Agregamos la pestaña de Entrevista como punto de inicio clínico
    t0, t1, t2, t3, t4 = st.tabs(["👤 ID", "💬 Entrevista", "🩺 Clínica", "📊 Antropo", "📝 Cierre"])

    with t0:
        nombre = st.text_input("Nombre del Paciente")
        c1, c2 = st.columns(2)
        edad = c1.text_input("Edad")
        domicilio = c2.text_input("Domicilio")
        interno = st.text_input("Interno(a) Responsable")

    with t1:
        st.subheader("Entrevista General")
        entrevista = st.text_area("Anamnesis / Motivo de consulta / Notas generales", height=200, help="Espacio para notas generales de la entrevista con el tutor/padre.")

    with t2:
        st.subheader("Valoración Clínica")
        tipo_alim = st.selectbox("Alimentación", ["LME", "LA", "LM+LA", "Complementaria"])
        obs_alim = st.text_area("Observaciones Alimentación")
        meds = st.text_area("Medicamentos / Suplementos")
        examenes = st.text_area("Vacunas / Exámenes / Instrumentos")

    with t3:
        st.subheader("Datos Antropométricos")
        ca, cb, cc = st.columns(3)
        peso, talla, pc = ca.text_input("Peso"), cb.text_input("Talla"), cc.text_input("PC")
        pe, te, pt = ca.text_input("P/E"), cb.text_input("T/E"), cc.text_input("P/T")
        diag = st.text_area("Diagnóstico Nutricional Integrado")

    with t4:
        st.subheader("Plan de Acción")
        ind = st.text_area("Indicaciones / Acuerdos")
        der = st.text_area("Derivaciones")

    enviar = st.form_submit_button("✨ FINALIZAR Y GENERAR REPORTE")

if enviar:
    if not nombre:
        st.error("⚠️ El nombre es obligatorio.")
    else:
        try:
            datos = {
                "nombre": nombre, "edad": edad, "domicilio": domicilio, "interno": interno,
                "entrevista": entrevista, "tipo_alim": tipo_alim, "obs_alim": obs_alim,
                "meds": meds, "examenes": examenes, "peso": peso, "talla": talla,
                "pc": pc, "pe": pe, "te": te, "pt": pt, "diag": diag, "ind": ind, "der": der
            }
            pdf_bytes = crear_pdf(datos)
            st.success("✅ ¡Ficha generada exitosamente!")
            st.download_button(label="📥 DESCARGAR PDF", data=bytes(pdf_bytes), file_name=f"Ficha_{nombre}.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Error: {e}")

# PIE DE PÁGINA
st.markdown("""
    <div class="footer-uoh">
        Sistema de Apoyo Clínico | Centro de Habilidades Clínicas y Disciplinares<br>
        <strong>Universidad de O'Higgins</strong>
    </div>
    """, unsafe_allow_html=True)
