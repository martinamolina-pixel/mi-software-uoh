import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="Software de Registro Clínico UOH", page_icon="🏥", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1 { color: #003366; font-family: 'Helvetica', sans-serif; }
    .stTabs [data-baseweb="tab"] { color: #003366; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #003366 !important; color: white !important; }
    .footer-uoh { text-align: center; color: #64748b; font-size: 0.8rem; border-top: 1px solid #e2e8f0; padding-top: 20px; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

NOMBRE_LOGO = "UOH - EsSa Azul (1) (3) (1).png"

if os.path.exists(NOMBRE_LOGO):
    st.image(NOMBRE_LOGO, width=400)
else:
    st.title("🏥 Sistema de Registro Clínico UOH")

st.markdown("### Registro Clinico | Internado APS - Evaluación")

# --- SELECTOR DE TIPO DE PACIENTE ---
tipo_paciente = st.selectbox("Seleccione el tipo de Registro Clínico:", ["Infantil / Adolescente", "Adulto / Adulto Mayor"])
st.write("---")

# --- CLASE PARA EL PDF ---
class ReporteClinico(FPDF):
    def header(self):
        if os.path.exists(NOMBRE_LOGO):
            self.image(NOMBRE_LOGO, 10, 8, 33)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, f'REGISTRO CLÍNICO - {tipo_paciente.upper()}', 0, 1, 'R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Centro de Habilidades Clínicas y Disciplinares - UOH', 0, 0, 'L')
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'R')

def crear_pdf(datos, tipo):
    pdf = ReporteClinico()
    pdf.add_page()
    
    def agregar_seccion(titulo, contenido):
        pdf.set_font("Arial", 'B', 10)
        pdf.set_fill_color(241, 245, 249)
        pdf.cell(0, 8, f" {titulo}", 1, 1, 'L', fill=True)
        pdf.set_font("Arial", '', 9)
        pdf.multi_cell(0, 6, str(contenido), 1)
        pdf.ln(3)

    agregar_seccion("I. IDENTIFICACIÓN", f"Paciente: {datos['nombre']}\nEdad: {datos['edad']}\nInterno Responsable: {datos['interno']}")
    agregar_seccion("II. ANAMNESIS / ENTREVISTA", datos['entrevista'])
    
    if tipo == "Infantil / Adolescente":
        agregar_seccion("III. VALORACIÓN CLÍNICA", f"Alimentación: {datos['tipo_alim']}\nMeds: {datos['meds']}\nInstrumentos: {datos['inst']}")
        agregar_seccion("IV. ANTROPOMETRÍA", f"Peso: {datos['peso']} kg | Talla: {datos['talla']} cm\nP/E: {datos['pe']} | T/E: {datos['te']} | P/T: {datos['pt']}\nDiag. Nutricional: {datos['diag']}")
    else:
        agregar_seccion("III. VALORACIÓN CLÍNICA ADULTO", f"Antecedentes: {datos['antecedentes']}\nFármacos: {datos['meds']}\nActividad Física: {datos['af']}")
        agregar_seccion("IV. ANTROPOMETRÍA ADULTO", f"Peso: {datos['peso']} kg | Talla: {datos['talla']} cm\nIMC: {datos['imc']} | C. Cintura: {datos['cc']}\nEstado Nutricional: {datos['estado']}")

    agregar_seccion("V. CIERRE", f"Indicaciones: {datos['ind']}\nDerivaciones: {datos['der']}")
    return pdf.output(dest='S')

# --- FORMULARIOS ---
with st.form("formulario_clinico"):
    t1, t_ent, t2, t3, t4 = st.tabs(["👤 ID", "💬 Entrevista", "🩺 Clínica", "📊 Antropo", "📝 Cierre"])

    with t1:
        nombre = st.text_input("Nombre del Paciente")
        edad = st.text_input("Edad")
        interno = st.text_input("Interno(a) Responsable")

    with t_ent:
        entrevista = st.text_area("Notas de la Entrevista / Motivo de consulta", height=150)

    with t2:
        if tipo_paciente == "Infantil / Adolescente":
            tipo_alim = st.selectbox("Alimentación", ["LME", "LA", "LM+LA", "Complementaria"])
            meds = st.text_area("Medicamentos / Vacunas")
            inst = st.text_area("Instrumentos (EEDP, TEPSI, etc.)")
        else:
            antecedentes = st.text_area("Antecedentes (HTA, DM2, DLP, etc.)")
            meds = st.text_area("Fármacos en uso")
            af = st.selectbox("Nivel Actividad Física", ["Sedentario", "Ligero", "Moderado", "Intenso"])

    with t3:
        col1, col2 = st.columns(2)
        peso = col1.text_input("Peso (kg)")
        talla = col2.text_input("Talla (cm)")
        if tipo_paciente == "Infantil / Adolescente":
            pe = col1.text_input("P/E")
            te = col2.text_input("T/E")
            pt = col1.text_input("P/T")
            diag = st.text_area("Diagnóstico Nutricional")
        else:
            imc = col1.text_input("IMC (Peso / Talla²)")
            cc = col2.text_input("Circunferencia Cintura (cm)")
            estado = st.selectbox("Estado Nutricional", ["Enflaquecido", "Normal", "Sobrepeso", "Obeso", "Obeso Mórbido"])

    with t4:
        ind = st.text_area("Acuerdos e Indicaciones")
        der = st.text_area("Derivaciones")

    enviar = st.form_submit_button("🚀 GENERAR REGISTRO")

if enviar:
    if not nombre or not interno:
        st.error("⚠️ Por favor complete el nombre del paciente y del interno.")
    else:
        try:
            # Diccionario base
            datos = {
                "nombre": nombre, "edad": edad, "interno": interno, "entrevista": entrevista,
                "peso": peso, "talla": talla, "ind": ind, "der": der, "meds": meds
            }
            # Agregar datos específicos
            if tipo_paciente == "Infantil / Adolescente":
                datos.update({"tipo_alim": tipo_alim, "inst": inst, "pe": pe, "te": te, "pt": pt, "diag": diag})
            else:
                datos.update({"antecedentes": antecedentes, "af": af, "imc": imc, "cc": cc, "estado": estado})

            pdf_bytes = crear_pdf(datos, tipo_paciente)
            st.success("✅ Registro generado correctamente.")
            
            # Nombre del archivo con el nombre del INTERNO
            nombre_archivo = f"Registro_{tipo_paciente.split()[0]}_{interno.replace(' ', '_')}.pdf"
            
            st.download_button(
                label="📥 DESCARGAR PDF",
                data=bytes(pdf_bytes),
                file_name=nombre_archivo,
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar reporte: {e}")

st.markdown("""
    <div class="footer-uoh">
        Sistema de Registro Clínico | Centro de Habilidades Clínicas y Disciplinares<br>
        <strong>Universidad de O'Higgins | Escuela de Salud</strong>
    </div>
    """, unsafe_allow_html=True)
