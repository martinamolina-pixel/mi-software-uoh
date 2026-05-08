import streamlit as st
from fpdf import FPDF
import os
from datetime import datetime

# 1. CONFIGURACIÓN E INTERFAZ MODERNA
st.set_page_config(page_title="Software de Registro Clínico UOH", page_icon="🏥", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    h1 { color: #003366; font-family: 'Helvetica', sans-serif; font-weight: bold; }
    .stTabs [data-baseweb="tab"] { color: #003366; font-weight: 600; border-radius: 8px; }
    .stTabs [aria-selected="true"] { background-color: #003366 !important; color: white !important; }
    .stForm { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# --- IDENTIDAD INSTITUCIONAL ---
NOMBRE_LOGO = "UOH - EsSa Azul (1) (3) (1).png"

if os.path.exists(NOMBRE_LOGO):
    st.image(NOMBRE_LOGO, width=400)
else:
    st.title("🏥 Sistema de Registro Clínico UOH")

st.markdown("### Internado APS - Evaluación Final de Asignatura")

# Selector principal
tipo_paciente = st.selectbox("Seleccione el tipo de Registro Clínico:", ["Infantil / Adolescente", "Adulto / Adulto Mayor"])
st.write("---")

# --- CLASE PARA EL PDF PROFESIONAL ---
class ReporteClinico(FPDF):
    def header(self):
        if os.path.exists(NOMBRE_LOGO):
            self.image(NOMBRE_LOGO, 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.set_text_color(0, 51, 102)
        self.cell(0, 5, 'REGISTRO CLÍNICO', 0, 1, 'R')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'EVALUACIÓN TEÓRICA PRÁCTICA FINAL DE LA ASIGNATURA', 0, 1, 'R')
        self.cell(0, 5, 'INTERNADO APS', 0, 1, 'R')
        self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Escuela de Salud - Universidad de O\'Higgins', 0, 0, 'L')
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'R')

def crear_pdf(datos, tipo):
    pdf = ReporteClinico()
    pdf.add_page()
    
    def agregar_seccion(titulo, contenido):
        pdf.set_font("Arial", 'B', 10)
        pdf.set_fill_color(230, 240, 250)
        pdf.cell(0, 8, f" {titulo}", 1, 1, 'L', fill=True)
        pdf.set_font("Arial", '', 9)
        pdf.multi_cell(0, 6, str(contenido), 1)
        pdf.ln(3)

    # I. IDENTIFICACIÓN (Igual para ambos)
    agregar_seccion("IDENTIFICACIÓN", 
                   f"Nombre Paciente: {datos['nombre']}\nEdad: {datos['edad']}\n"
                   f"Domicilio: {datos['domicilio']}\nNombre Interno Enfermería: {datos['interno']}")
    
    # II. ENTREVISTA
    agregar_seccion("ENTREVISTA", datos['entrevista'])
    
    if tipo == "Infantil / Adolescente":
        # Bloque Pediátrico
        agregar_seccion("TIPO ALIMENTACIÓN", f"Estado: {datos['tipo_alim']}\nObservaciones: {datos['obs_alim']}")
        agregar_seccion("MEDICAMENTOS / SUPLEMENTOS", datos['meds'])
        agregar_seccion("VACUNAS / EXÁMENES / RADIOGRAFÍAS", datos['examenes'])
        agregar_seccion("INSTRUMENTOS / RESULTADOS", datos['inst'])
        agregar_seccion("ANTROPOMETRÍA", 
                       f"Peso: {datos['peso']} | Talla: {datos['talla']} | Perímetro Craneano: {datos['pc']}\n"
                       f"P/E: {datos['pe']} | T/E: {datos['te']} | P/T: {datos['pt']}\n"
                       f"Diagnóstico Nutricional: {datos['diag']}")
    else:
        # Bloque Adulto
        agregar_seccion("ANTROPOMETRÍA", 
                       f"Peso: {datos['peso']} | Talla: {datos['talla']}\nIMC: {datos['imc']} | CC: {datos['cc']}")
        agregar_seccion("CONTROL DE SIGNOS VITALES", 
                       f"PA: {datos['pa']} | FC: {datos['fc']} | PULSO: {datos['pulso']} | FR: {datos['fr']}")
        agregar_seccion("EXÁMENES RELEVANTES", datos['examenes'])

    # Cierre (Igual para ambos)
    agregar_seccion("ACUERDOS E INDICACIONES", datos['ind'])
    agregar_seccion("DERIVACIONES", datos['der'])
    
    return pdf.output(dest='S')

# --- FORMULARIO DE ENTRADA ---
with st.form("registro_maestro"):
    t1, t2, t3, t4, t5 = st.tabs(["👤 Identificación", "💬 Entrevista", "🩺 Clínica", "📊 Antropo", "📝 Cierre"])

    with t1:
        nombre = st.text_input("Nombre del Paciente")
        col_id1, col_id2 = st.columns(2)
        edad = col_id1.text_input("Edad")
        domicilio = col_id2.text_input("Domicilio")
        interno = st.text_input("Nombre Interno(a) Enfermería")

    with t2:
        entrevista = st.text_area("Entrevista", height=200)

    with t3:
        if tipo_paciente == "Infantil / Adolescente":
            tipo_alim = st.radio("Tipo Alimentación", ["LME", "LA", "LM+LA", "COMPLEMENTARIA"], horizontal=True)
            obs_alim = st.text_area("Observaciones Alimentación")
            meds = st.text_area("Medicamentos / Suplementos")
            examenes = st.text_area("Vacunas / Exámenes / Radiografías")
            inst = st.text_area("Instrumentos / Resultados")
        else:
            st.subheader("Control de Signos Vitales")
            c_sv1, c_sv2 = st.columns(2)
            pa = c_sv1.text_input("PA")
            fc = c_sv2.text_input("FC")
            pulso = c_sv1.text_input("PULSO")
            fr = c_sv2.text_input("FR")
            examenes = st.text_area("Exámenes Relevantes")

    with t4:
        st.subheader("Antropometría")
        c_ant1, c_ant2, c_ant3 = st.columns(3)
        peso = c_ant1.text_input("Peso")
        talla = c_ant2.text_input("Talla")
        
        if tipo_paciente == "Infantil / Adolescente":
            pc = c_ant3.text_input("Perímetro Craneano")
            pe = c_ant1.text_input("P/E")
            te = c_ant2.text_input("T/E")
            pt = c_ant3.text_input("P/T")
            diag = st.text_area("Diagnóstico Nutricional")
        else:
            imc = c_ant1.text_input("IMC")
            cc = c_ant2.text_input("CC")

    with t5:
        ind = st.text_area("Acuerdos e Indicaciones")
        der = st.text_area("Derivaciones")

    enviar = st.form_submit_button("🚀 GENERAR REGISTRO")

if enviar:
    if not nombre or not interno:
        st.error("⚠️ Ingrese Nombre del Paciente e Interno.")
    else:
        try:
            # Diccionario base con Domicilio incluido
            datos = {
                "nombre": nombre, "edad": edad, "domicilio": domicilio, "interno": interno,
                "entrevista": entrevista, "peso": peso, "talla": talla, "ind": ind, "der": der
            }
            
            if tipo_paciente == "Infantil / Adolescente":
                datos.update({
                    "tipo_alim": tipo_alim, "obs_alim": obs_alim, "meds": meds, 
                    "examenes": examenes, "inst": inst, "pc": pc, "pe": pe, "te": te, "pt": pt, "diag": diag
                })
            else:
                datos.update({
                    "imc": imc, "cc": cc, "pa": pa, "fc": fc, "pulso": pulso, "fr": fr, "examenes": examenes
                })

            pdf_out = crear_pdf(datos, tipo_paciente)
            st.success(f"✅ Registro de {tipo_paciente} generado.")
            
            # Descarga con nombre del INTERNO
            st.download_button(
                label="📥 DESCARGAR PDF",
                data=bytes(pdf_out),
                file_name=f"Registro_Interno_{interno.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown(f"""<div class="footer-uoh">Universidad de O'Higgins | Escuela de Salud<br>Fecha: {datetime.now().strftime('%d/%m/%Y')}</div>""", unsafe_allow_html=True)
