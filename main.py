import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# 1. CONFIGURACIÓN ESTÉTICA PROFESIONAL
st.set_page_config(
    page_title="Registro Clínico UOH",
    page_icon="🏥",
    layout="centered"
)

# Estilo CSS para colores institucionales y mejor legibilidad
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1 { color: #003366; font-family: 'Helvetica', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 4px 4px 0 0;
        padding: 10px 15px;
        color: #003366;
    }
    .stTabs [aria-selected="true"] {
        background-color: #003366 !important;
        color: white !important;
    }
    .footer-uoh {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        border-top: 1px solid #e2e8f0;
        padding-top: 20px;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CABECERA E IDENTIDAD ---
NOMBRE_LOGO = "UOH - EsSa Azul (1) (3) (1).png"

if os.path.exists(NOMBRE_LOGO):
    st.image(NOMBRE_LOGO, width=400)
else:
    st.title("🏥 Sistema de Registro Clínico")

st.markdown("### Registro Clínico Adulto | Internado APS - Evaluación")
st.write("---")

# --- CLASE PARA EL PDF PROFESIONAL ---
class ReporteClinico(FPDF):
    def header(self):
        if os.path.exists(NOMBRE_LOGO):
            self.image(NOMBRE_LOGO, 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 51, 102) # Azul UOH
        self.cell(0, 10, 'FICHA DE ATENCIÓN CLÍNICA', 0, 1, 'R')
        self.set_draw_color(0, 51, 102)
        self.line(10, 25, 200, 25)
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
    
    def agregar_seccion(titulo, contenido):
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(241, 245, 249)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 9, f" {titulo}", 1, 1, 'L', fill=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(30, 41, 59)
        pdf.multi_cell(0, 7, str(contenido), 1)
        pdf.ln(4)

    agregar_seccion("I. IDENTIFICACIÓN DEL PACIENTE", 
                   f"Nombre: {datos['nombre']}\nEdad: {datos['edad']}\nDomicilio: {datos['domicilio']}\n"
                   f"Responsable: {datos['interno']}\nFecha: {datetime.now().strftime('%d/%m/%Y')}")

    agregar_seccion("II. ANAMNESIS / ENTREVISTA", datos['entrevista'])

    agregar_seccion("II. VALORACIÓN CLÍNICA", 
                   f"Alimentación: {datos['tipo_alim']}\nObservaciones: {datos['obs_alim']}\n"
                   f"Medicamentos: {datos['meds']}\nExámenes/ Vacunas / Radiografías: {datos['examenes']}\n"
                   f"Instrumentos / Resultados: {datos['inst']}")
    
    agregar_seccion("III. ANTROPOMETRÍA Y DIAGNÓSTICO", 
                   f"Peso: {datos['peso']} kg | Talla: {datos['talla']} cm | PC: {datos['pc']} cm\n"
                   f"Indicadores: P/E: {datos['pe']} | T/E: {datos['te']} | P/T: {datos['pt']}\n"
                   f"Diagnóstico: {datos['diag']}")
    
    agregar_seccion("IV. INDICACIONES Y CIERRE", 
                   f"Acuerdos: {datos['ind']}\nDerivaciones: {datos['der']}")
    
    # Retornar como bytes directamente para evitar errores de codificación
    return pdf.output(dest='S')

# --- INTERFAZ DE USUARIO ---
with st.form("formulario_clinico_uoh"):
    # Segmentos organizados
# Agregamos "💬 Entrevista" en la lista de pestañas
    tab1, tab_ent, tab2, tab3, tab4 = st.tabs(["👤 Identificación", "💬 Entrevista", "🩺 Clínica", "📊 Antropometría", "📝 Cierre"])

    with tab_ent:
        st.subheader("Entrevista / Anamnesis")
        entrevista = st.text_area("Notas generales de la entrevista y motivo de consulta", height=200)

    with tab1:
        nombre = st.text_input("Nombre del Paciente")
        c1, c2 = st.columns(2)
        edad = c1.text_input("Edad")
        domicilio = c2.text_input("Domicilio")
        interno = st.text_input("Interno(a) Responsable")

    with tab2:
        tipo_alim = st.selectbox("Tipo de Alimentación", ["LME", "LA", "LM+LA", "Complementaria"])
        obs_alim = st.text_area("Observaciones Alimentación")
        meds = st.text_area("Medicamentos / Suplementos")
        examenes = st.text_area("Vacunas / Exámenes")
        inst = st.text_area("Instrumentos / Resultados")

    with tab3:
        ca, cb, cc = st.columns(3)
        peso, talla, pc = ca.text_input("Peso"), cb.text_input("Talla"), cc.text_input("PC")
        pe, te, pt = ca.text_input("P/E"), cb.text_input("T/E"), cc.text_input("P/T")
        diag = st.text_area("Diagnóstico Nutricional")

    with tab4:
        ind = st.text_area("Acuerdos e Indicaciones")
        der = st.text_area("Derivaciones")

    # Botón de envío corregido
    enviar = st.form_submit_button("🚀 GENERAR REGISTRO CLÍNICO")

if enviar:
    if not nombre:
        st.error("⚠️ Ingrese el nombre del paciente.")
    else:
        try:
            datos = {
                "nombre": nombre, "edad": edad, "domicilio": domicilio, "interno": interno,
                "entrevista": entrevista,
                "tipo_alim": tipo_alim, "obs_alim": obs_alim, "meds": meds, "examenes": examenes,
                "inst": inst, "peso": peso, "talla": talla, "pc": pc, "pe": pe, "te": te,
                "pt": pt, "diag": diag, "ind": ind, "der": der
            }
            
            # Generar PDF y descargar
            pdf_bytes = crear_pdf(datos)
            st.success("✅ Registro generado exitosamente.")
            st.download_button(
                label="📥 DESCARGAR FICHA EN PDF",
                data=bytes(pdf_bytes),
                file_name=f"Ficha_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar reporte: {e}")

# PIE DE PÁGINA INSTITUCIONAL
st.markdown("""
    <div class="footer-uoh">
        Sistema generado por el Centro de Habilidades Clínicas y Disciplinares<br>
        <strong>Universidad de O'Higgins | Escuela de Salud</strong>
    </div>
    """, unsafe_allow_html=True)
