import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# 1. CONFIGURACIÓN ESTÉTICA
st.set_page_config(page_title="Registro Clínico UOH", page_icon="🏥", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    h1 { color: #003366; font-family: 'Segoe UI', sans-serif; font-weight: 800; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        padding: 12px 20px;
        font-weight: 600;
        color: #003366;
    }
    .stTabs [aria-selected="true"] {
        background-color: #003366 !important;
        color: white !important;
    }
    .footer-uoh {
        text-align: center;
        color: #475569;
        font-size: 0.85rem;
        border-top: 2px solid #003366;
        padding-top: 20px;
        margin-top: 60px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
NOMBRE_LOGO = "UOH - EsSa Azul (1) (3) (1).png"

if os.path.exists(NOMBRE_LOGO):
    st.image(NOMBRE_LOGO, width=420)
else:
    st.title("🏥 SISTEMA DE REGISTRO CLÍNICO")

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

    sec("I. IDENTIFICACIÓN", f"Paciente: {datos['nombre']}\nEdad: {datos['edad']}\nInterno: {datos['interno']}")
    sec("II. ENTREVISTA GENERAL", datos['entrevista'])
    sec("III. VALORACIÓN CLÍNICA", f"Alimentación: {datos['tipo_alim']}\nObs. Alimentación: {datos['obs_alim']}\nMedicamentos: {datos['meds']}\nExámenes/Vacunas: {datos['examenes']}")
    sec("IV. INSTRUMENTOS Y RESULTADOS", datos['inst']) # SECCIÓN NUEVA EN PDF
    sec("V. ANTROPOMETRÍA", f"Peso: {datos['peso']} kg | Talla: {datos['talla']} cm | PC: {datos['pc']} cm\nP/E: {datos['pe']} | T/E: {datos['te']} | P/T: {datos['pt']}\nDiagnóstico: {datos['diag']}")
    sec("VI. ACUERDOS Y DERIVACIONES", f"Indicaciones: {datos['ind']}\nDerivaciones: {datos['der']}")
    
    return pdf.output(dest='S')

# --- FORMULARIO ---
with st.form("registro_final_martina"):
    t0, t1, t2, t3, t4 = st.tabs(["👤 ID", "💬 Entrevista", "🩺 Clínica", "📊 Antropo", "📝 Cierre"])

    with t0:
        nombre = st.text_input("Nombre del Paciente")
        c1, c2 = st.columns(2)
        edad = c1.text_input("Edad")
        domicilio = c2.text_input("Domicilio")
        interno = st.text_input("Interno(a) Responsable")

    with t1:
        st.subheader("Entrevista General")
        entrevista = st.text_area("Anamnesis / Motivo de consulta", height
