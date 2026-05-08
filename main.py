import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# 1. ESTÉTICA Y CONFIGURACIÓN (McKinsey Style)
st.set_page_config(
    page_title="Sistema de Registro Clínico - UOH",
    page_icon="🏥",
    layout="centered"
)

# Colores institucionales y estilo CSS personalizado
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        font-weight: bold;
        color: #003366;
    }
    .stTabs [aria-selected="true"] {
        background-color: #003366 !important;
        color: white !important;
    }
    h1 { color: #003366; font-family: 'Poppins', sans-serif; font-weight: 700; }
    h3 { color: #003366; border-bottom: 2px solid #11CAA0; padding-bottom: 5px; }
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 20px;
        width: 100%;
        font-weight: bold;
        padding: 15px;
    }
    .footer-text {
        text-align: center;
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_ Harris=True)

# --- MANEJO DEL LOGO (Nombre exacto de tu archivo en GitHub) ---
NOMBRE_LOGO = "UOH - EsSa Azul (1) (3) (1).png"

def mostrar_cabecera():
    if os.path.exists(NOMBRE_LOGO):
        st.image(NOMBRE_LOGO, width=400)
    else:
        st.title("🏥 REGISTRO CLÍNICO UOH")
    st.markdown("### Escuela de Salud | Internado APS")
    st.write("---")

mostrar_cabecera()

# --- CLASE PARA EL REPORTE PDF (Diseño Profesional) ---
class ReporteClinico(FPDF):
    def header(self):
        if os.path.exists(NOMBRE_LOGO):
            self.image(NOMBRE_LOGO, 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 51, 102) # Azul UOH
        self.cell(0, 10, 'REPORTE DE ATENCIÓN CLÍNICA', 0, 1, 'R')
        self.set_draw_color(17, 202, 160) # Verde Clínico
        self.line(10, 25, 200, 25)
        self.ln(12)

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 116, 139)
        self.line(10, 275, 200, 275)
        self.cell(0, 10, 'Centro de Habilidades Clínicas y Disciplinares - Universidad de O\'Higgins', 0, 0, 'L')
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'R')

def generar_pdf_pro(datos):
    pdf = ReporteClinico()
    pdf.add_page()
    
    def bloque_info(titulo, contenido):
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(241, 245, 249)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 9, f" {titulo}", 1, 1, 'L', fill=True)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(51, 65, 85)
        pdf.multi_cell(0, 7, str(contenido), 1)
        pdf.ln(5)

    # Llenado de Secciones
    bloque_info("I. IDENTIFICACIÓN GENERAL", 
               f"Nombre Paciente: {datos['nombre']}\n"
               f"Edad: {datos['edad']} | Domicilio: {datos['domicilio']}\n"
               f"Interno(a) Responsable: {datos['interno']}\n"
               f"Fecha de Atención: {datetime.now().strftime('%d/%m/%Y')}")
    
    bloque_info("II. ANÁLISIS DE ALIMENTACIÓN Y ENTREVISTA", 
               f"Tipo de Alimentación: {datos['tipo_alim']}\n"
               f"Observaciones: {datos['obs_alim']}")
    
    bloque_info("III. ANTECEDENTES CLÍNICOS Y EXÁMENES", 
               f"Medicamentos/Suplementos: {datos['meds']}\n"
               f"Vacunas/Exámenes: {datos['examenes']}\n"
               f"Instrumentos Aplicados: {datos['inst']}")
    
    bloque_info("IV. EVALUACIÓN ANTROPOMÉTRICA", 
               f"Peso: {datos['peso']} kg | Talla: {datos['talla']} cm | P. Craneano: {datos['pc']} cm\n"
               f"Indicadores: P/E: {datos['pe']} | T/E: {datos['te']} | P/T: {datos['pt']}\n"
               f"Diagnóstico Nutricional: {datos['diag']}")
    
    bloque_info("V. PLAN DE CIERRE E INDICACIONES", 
               f"Acuerdos e Indicaciones: {datos['ind']}\n"
               f"Derivaciones: {datos['der']}")
    
    return pdf.output()

# --- INTERFAZ POR SEGMENTOS (Tabs) ---
with st.form("software_clinico_uoh"):
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Identificación", "🩺 Clínica", "📊 Antropometría", "📝 Cierre"
    ])

    with tab1:
        st.subheader("Datos del Paciente")
        nombre = st.text_input("Nombre Completo")
        c1, c2 = st.columns(2)
        edad = c1.text_input("Edad (ej: 5 años 2 meses)")
        domicilio = c2.text_input("Domicilio / Comuna")
        interno = st.text_input("Interno(a) de Enfermería en práctica")

    with tab2:
        st.subheader("Evaluación de Ingreso")
        tipo_alim = st.selectbox("Esquema Alimentario", ["LME", "LA", "LM+LA", "COMPLEMENTARIA", "SÓLIDOS"])
        obs_alim = st.text_area("Observaciones de Alimentación", placeholder="Detalle frecuencia, volúmenes, etc.")
        meds = st.text_area("Farmacoterapia / Suplementos")
        examenes = st.text_area("Vacunas / Exámenes / Radiografías")
        inst = st.text_area("Instrumentos / Resultados (EEDP, TEPSI, Score, etc.)")

    with tab3:
        st.subheader("Parámetros Biométricos")
        ca, cb, cc = st.columns(3)
        peso, talla, pc = ca.text_input("Peso (kg)"), cb.text_input("Talla (cm)"), cc.text_input("P.C. (cm)")
        st.write("---")
        st.caption("Indicadores de Crecimiento")
        pe, te, pt = ca.text_input("P/E"), cb.text_input("T/E"), cc.text_input("P/T")
        diag = st.text_area("Diagnóstico Nutricional Integrado")

    with tab4:
        st.subheader("Plan de Acción")
        ind = st.text_area("Acuerdos e Indicaciones para el cuidador")
        der = st.text_area("Derivaciones / Interconsultas")

    # Botón principal estilizado
    submit_btn = st.form_submit_button("🚀 GENERAR REGISTRO DIGITAL")

# --- PROCESAMIENTO FINAL ---
if submit_btn:
    if not nombre:
        st.warning("⚠️ El nombre del paciente es obligatorio para el registro.")
    else:
        try:
            datos_finales = {
                "nombre": nombre, "edad": edad, "domicilio": domicilio, "interno": interno,
                "tipo_alim": tipo_alim, "obs_alim": obs_alim, "meds": meds, "examenes": examenes,
                "inst": inst, "peso": peso, "talla": talla, "pc": pc, "pe": pe, "te": te,
                "pt": pt, "diag": diag, "ind": ind, "der": der
            }
            
            pdf_data = generar_pdf_pro(datos_finales)
            
            st.success("✅ ¡Registro generado con éxito! Puede descargar el informe profesional abajo.")
            st.download_button(
                label="📥 DESCARGAR INFORME CLÍNICO PDF",
                data=bytes(pdf_data),
                file_name=f"Registro_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Falla en la generación del reporte: {e}")

# Pie de página institucional
st.markdown(f"""
    <div class="footer-text">
        Sistema generado por el <strong>Centro de Habilidades Clínicas y Disciplinares</strong><br>
        Universidad de O'Higgins | Escuela de Salud<br>
        Internado APS - {datetime.now().year}
    </div>
    """, unsafe_allow_html=True)

¡Espero que esta versión te encante! Es mucho más vistosa, usa los colores azules de la UOH de forma elegante y mantiene todo el rigor clínico que requiere tu examen. ¡Mucho éxito mañana, Martina! Cualquier duda extra, aquí estoy.
