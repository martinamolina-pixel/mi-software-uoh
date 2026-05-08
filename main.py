import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Registro Clínico UOH", page_icon="🏥", layout="centered")

# Estilo visual institucional
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        color: #003366;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #003366 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA ---
# Usamos el nombre exacto del archivo que tienes en tu GitHub
NOMBRE_LOGO = "UOH - EsSa Azul (1) (3) (1).png"

if os.path.exists(NOMBRE_LOGO):
    st.image(NOMBRE_LOGO, width=400)
else:
    st.title("🏥 Sistema de Registro Clínico")
    st.write("Escuela de Salud - UOH")

st.write("---")

# --- CLASE PARA EL PDF ---
class PDF(FPDF):
    def header(self):
        if os.path.exists(NOMBRE_LOGO):
            self.image(NOMBRE_LOGO, 10, 8, 33)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(0, 51, 102)
        self.cell(0, 5, 'REGISTRO CLÍNICO', 0, 1, 'C')
        self.set_font('Arial', '', 8)
        self.cell(0, 5, 'EVALUACIÓN TEÓRICA PRÁCTICA FINAL DE LA ASIGNATURA', 0, 1, 'C')
        self.cell(0, 5, 'INTERNADO APS', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generar_pdf(d):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 9)
    
    # Tabla de Identificación
    pdf.set_fill_color(240, 240, 240)
    def fila(label, valor):
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(50, 7, label, 1, 0, 'L', fill=True)
        pdf.set_font("Arial", '', 9)
        pdf.cell(140, 7, str(valor), 1, 1, 'L')

    fila("Nombre Paciente", d['nombre'])
    fila("Edad", d['edad'])
    fila("Domicilio", d['domicilio'])
    fila("Nombre Interno Enfermería", d['interno'])
    pdf.ln(5)

    # Secciones de texto
    def seccion(titulo, contenido):
        pdf.set_font("Arial", 'B', 9)
        pdf.set_fill_color(230, 235, 245)
        pdf.cell(0, 7, titulo, 1, 1, 'L', fill=True)
        pdf.set_font("Arial", '', 9)
        pdf.multi_cell(0, 7, str(contenido), 1)
        pdf.ln(3)

    seccion("ENTREVISTA", d['entrevista'])
    
    # Tabla Alimentación
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 7, "TIPO ALIMENTACIÓN", 1, 1, 'L', fill=True)
    pdf.cell(47.5, 7, "LME", 1, 0, 'C')
    pdf.cell(47.5, 7, "LA", 1, 0, 'C')
    pdf.cell(47.5, 7, "LM+LA", 1, 0, 'C')
    pdf.cell(47.5, 7, "COMPLEMENTARIA", 1, 1, 'C')
    
    # Marcar opción elegida
    pdf.cell(47.5, 7, "X" if d['tipo']=="LME" else "", 1, 0, 'C')
    pdf.cell(47.5, 7, "X" if d['tipo']=="LA" else "", 1, 0, 'C')
    pdf.cell(47.5, 7, "X" if d['tipo']=="LM+LA" else "", 1, 0, 'C')
    pdf.cell(47.5, 7, "X" if d['tipo']=="Complementaria" else "", 1, 1, 'C')
    
    seccion("Observaciones Alimentación", d['obs_alim'])
    seccion("MEDICAMENTOS/SUPLEMENTOS", d['meds'])
    seccion("VACUNAS/ EXÁMENES /RADIOGRAFÍAS", d['examenes'])
    seccion("INSTRUMENTOS/RESULTADOS (EEDP, Score, etc)", d['inst'])
    
    # Antropometría
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 7, "ANTROPOMETRÍA", 1, 1, 'L', fill=True)
    pdf.cell(63, 7, f"Peso: {d['peso']} kg", 1, 0)
    pdf.cell(63, 7, f"Talla: {d['talla']} cm", 1, 0)
    pdf.cell(64, 7, f"PC: {d['pc']} cm", 1, 1)
    pdf.cell(63, 7, f"P/E: {d['pe']}", 1, 0)
    pdf.cell(63, 7, f"T/E: {d['te']}", 1, 0)
    pdf.cell(64, 7, f"P/T: {d['pt']}", 1, 1)
    
    seccion("Diagnóstico Nutricional", d['diag'])
    seccion("ACUERDOS E INDICACIONES", d['ind'])
    seccion("DERIVACIONES", d['der'])

    return pdf.output(dest='S')

# --- FORMULARIO STREAMLIT ---
with st.form("ficha_uoh"):
    t1, t2, t3, t4, t5 = st.tabs(["👤 ID", "💬 Entrevista", "🩺 Clínica", "📊 Antropo", "📝 Cierre"])
    
    with t1:
        nombre = st.text_input("Nombre del Paciente")
        c1, c2 = st.columns(2)
        edad = c1.text_input("Edad")
        domicilio = c2.text_input("Domicilio")
        interno = st.text_input("Interno(a) Responsable")

    with t2:
        entrevista = st.text_area("Entrevista / Notas Generales", height=200)

    with t3:
        tipo = st.selectbox("Tipo de Alimentación", ["LME", "LA", "LM+LA", "Complementaria"])
        obs_alim = st.text_area("Observaciones Alimentación")
        meds = st.text_area("Medicamentos / Suplementos")
        examenes = st.text_area("Vacunas / Exámenes")
        inst = st.text_area("Instrumentos y Resultados (EEDP, Score, etc.)")

    with t4:
        c3, c4, c5 = st.columns(3)
        peso = c3.text_input("Peso (kg)")
        talla = c4.text_input("Talla (cm)")
        pc = c5.text_input("PC (cm)")
        pe = c3.text_input("P/E")
        te = c4.text_input("T/E")
        pt = c5.text_input("P/T")
        diag = st.text_area("Diagnóstico Nutricional")

    with t5:
        ind = st.text_area("Acuerdos e Indicaciones")
        der = st.text_area("Derivaciones")

    enviar = st.form_submit_button("💾 GENERAR REGISTRO")

if enviar:
    if not nombre:
        st.error("⚠️ Ingrese el nombre del paciente.")
    else:
        try:
            datos = {
                "nombre": nombre, "edad": edad, "domicilio": domicilio, "interno": interno,
                "entrevista": entrevista, "tipo": tipo, "obs_alim": obs_alim,
                "meds": meds, "examenes": examenes, "inst": inst,
                "peso": peso, "talla": talla, "pc": pc, "pe": pe, "te": te, "pt": pt,
                "diag": diag, "ind": ind, "der": der
            }
            pdf_out = generar_pdf(datos)
            st.success("✅ ¡Ficha lista!")
            st.download_button(
                label="📥 DESCARGAR PDF",
                data=bytes(pdf_out),
                file_name=f"Ficha_{nombre}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al crear PDF: {e}")
