import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Registro Clínico APS - UOH", layout="centered")

class PDF(FPDF):
    def header(self):
        # Intento de cargar logo institucional
        try:
            # URL de descarga directa del logo que enviaste
            logo_url = "https://drive.google.com/uc?id=1im706wttlyX4vA5v_gWcmBAg5KRSbH6r"
            self.image(logo_url, 10, 8, 33)
        except:
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'UNIVERSIDAD DE O\'HIGGINS', 0, 1, 'L')
            
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'REGISTRO CLÍNICO - INTERNADO APS', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'EVALUACIÓN TEÓRICA PRÁCTICA FINAL', 0, 1, 'C')
        self.ln(10)

    def seccion_titulo(self, titulo):
        self.set_font('Arial', 'B', 11)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, titulo, 1, 1, 'L', fill=True)
        self.set_font('Arial', '', 10)

def generar_ficha_pdf(d):
    pdf = PDF()
    pdf.add_page()
    
    # 1. IDENTIFICACIÓN
    pdf.seccion_titulo("I. IDENTIFICACIÓN")
    pdf.multi_cell(0, 7, f"Nombre Paciente: {d['nombre']}\nEdad: {d['edad']}\nDomicilio: {d['domicilio']}\nInterno de Enfermería: {d['interno']}", 1)
    pdf.ln(4)
    
    # 2. ENTREVISTA Y ALIMENTACIÓN
    pdf.seccion_titulo("II. ENTREVISTA Y ALIMENTACIÓN")
    pdf.multi_cell(0, 7, f"Tipo Alimentación: {d['tipo_alim']}\nObservaciones: {d['obs_alim']}", 1)
    pdf.ln(4)
    
    # 3. CLÍNICA Y EXÁMENES
    pdf.seccion_titulo("III. HISTORIA CLÍNICA")
    pdf.multi_cell(0, 7, f"Medicamentos/Suplementos: {d['meds']}\nVacunas/Exámenes/Radiografías: {d['examenes']}\nInstrumentos/Resultados: {d['inst']}", 1)
    pdf.ln(4)
    
    # 4. ANTROPOMETRÍA
    pdf.seccion_titulo("IV. ANTROPOMETRÍA Y DIAGNÓSTICO")
    # Usamos una sola celda para evitar el error de espacio horizontal
    antropo = f"Peso: {d['peso']} | Talla: {d['talla']} | P. Craneano: {d['pc']}\n"
    antropo += f"P/E: {d['pe']} | T/E: {d['te']} | P/T: {d['pt']}\n"
    antropo += f"Diagnóstico Nutricional: {d['diag']}"
    pdf.multi_cell(0, 7, antropo, 1)
    pdf.ln(4)
    
    # 5. CIERRE
    pdf.seccion_titulo("V. ACUERDOS E INDICACIONES")
    pdf.multi_cell(0, 7, f"Indicaciones: {d['ind']}\nDerivaciones: {d['der']}", 1)
    
    return pdf.output()

# --- INTERFAZ STREAMLIT ---
st.title("🏥 Registro Clínico APS")
st.info("Complete los campos para generar la ficha oficial")

with st.form("ficha_uoh"):
    tab1, tab2, tab3 = st.tabs(["👤 Identificación", "🩺 Clínica", "📊 Antropometría"])
    
    with tab1:
        nombre = st.text_input("Nombre Paciente")
        edad = st.text_input("Edad")
        domicilio = st.text_input("Domicilio")
        interno = st.text_input("Interno(a) Enfermería")
        
    with tab2:
        tipo_alim = st.selectbox("Tipo Alimentación", ["LME", "LA", "LM+LA", "COMPLEMENTARIA"])
        obs_alim = st.text_area("Observaciones Alimentación")
        meds = st.text_area("Medicamentos/Suplementos")
        examenes = st.text_area("Vacunas/Exámenes/Radiografías")
        inst = st.text_area("Instrumentos/Resultados (EEDP, Score, etc.)")
        
    with tab3:
        c1, c2, c3 = st.columns(3)
        peso = c1.text_input("Peso")
        talla = c2.text_input("Talla")
        pc = c3.text_input("P. Craneano")
        pe = c1.text_input("P/E")
        te = c2.text_input("T/E")
        pt = c3.text_input("P/T")
        diag = st.text_area("Diagnóstico Nutricional")
        ind = st.text_area("Acuerdos e Indicaciones")
        der = st.text_area("Derivaciones")

    enviar = st.form_submit_button("🚀 GENERAR REGISTRO COMPLETO")

if enviar:
    if not nombre:
        st.warning("Escriba el nombre del paciente.")
    else:
        # Diccionario de datos
        datos = {
            "nombre": nombre, "edad": edad, "domicilio": domicilio, "interno": interno,
            "tipo_alim": tipo_alim, "obs_alim": obs_alim, "meds": meds, "examenes": examenes,
            "inst": inst, "peso": peso, "talla": talla, "pc": pc, "pe": pe, "te": te,
            "pt": pt, "diag": diag, "ind": ind, "der": der
        }
        
        try:
            pdf_bytes = generar_ficha_pdf(datos)
            st.success("✅ Ficha generada correctamente")
            st.download_button(
                label="📥 DESCARGAR FICHA PDF",
                data=bytes(pdf_bytes),
                file_name=f"Ficha_{nombre.replace(' ','_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error técnico: {e}")
