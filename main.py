import streamlit as st
from fpdf import FPDF
from datetime import datetime

# 1. Configuración de página
st.set_page_config(page_title="Registro Clínico UOH", page_icon="🏥", layout="centered")

# --- FUNCIÓN PARA GENERAR EL PDF ---
class PDF(FPDF):
    def header(self):
        # Nuevo Logo con link de descarga directa
        try:
            logo_url = "https://drive.google.com/uc?id=1QD40i4hMpGqGxpx7Zaw8JLad3CwPHo_x"
            self.image(logo_url, 10, 8, 33)
        except:
            pass
        
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'REGISTRO CLÍNICO - INTERNADO APS', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'EVALUACIÓN TEÓRICA PRÁCTICA FINAL', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        # Créditos al final del informe PDF
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Sistema generado por el Centro de Habilidades Clínicas y Disciplinares - UOH', 0, 0, 'C')

def generar_pdf_integral(d):
    pdf = PDF()
    pdf.add_page()
    
    def agregar_bloque(pdf, titulo, contenido):
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, titulo, 1, 1, 'L', fill=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 7, contenido, 1)
        pdf.ln(4)

    agregar_bloque(pdf, "I. IDENTIFICACIÓN", f"Paciente: {d['nombre']}\nEdad: {d['edad']}\nDomicilio: {d['domicilio']}\nInterno(a): {d['interno']}")
    agregar_bloque(pdf, "II. ENTREVISTA Y ALIMENTACIÓN", f"Tipo Alimentación: {d['tipo_alim']}\nObservaciones: {d['obs_alim']}")
    agregar_bloque(pdf, "III. MEDICAMENTOS Y EXÁMENES", f"Meds/Suplementos: {d['meds']}\nVacunas/Exámenes: {d['examenes']}\nInstrumentos: {d['inst']}")
    agregar_bloque(pdf, "IV. ANTROPOMETRÍA", f"Peso: {d['peso']} | Talla: {d['talla']} | PC: {d['pc']}\nP/E: {d['pe']} | T/E: {d['te']} | P/T: {d['pt']}\nDiagnóstico Nutricional: {d['diag']}")
    agregar_bloque(pdf, "V. PLAN DE CIERRE", f"Indicaciones: {d['ind']}\nDerivaciones: {d['der']}")
    
    return pdf.output()

# --- INTERFAZ DEL SOFTWARE ---

# Logo Superior
st.image("https://drive.google.com/uc?id=1QD40i4hMpGqGxpx7Zaw8JLad3CwPHo_x", width=250)
st.title("Sistema de Registro Clínico")

with st.form("registro_software"):
    # Separación por segmentos (Pestañas)
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Identificación", "🩺 Clínica", "📊 Antropometría", "📝 Cierre"])

    with tab1:
        nombre = st.text_input("Nombre del Paciente")
        col_id = st.columns(2)
        edad = col_id[0].text_input("Edad")
        domicilio = col_id[1].text_input("Domicilio")
        interno = st.text_input("Nombre Interno(a) Enfermería")

    with tab2:
        tipo_alim = st.selectbox("Tipo Alimentación", ["LME", "LA", "LM+LA", "COMPLEMENTARIA"])
        obs_alim = st.text_area("Observaciones Alimentación")
        meds = st.text_area("Medicamentos/Suplementos")
        examenes = st.text_area("Vacunas / Exámenes / Radiografías")
        inst = st.text_area("Instrumentos / Resultados")

    with tab3:
        c1, c2, c3 = st.columns(3)
        peso, talla, pc = c1.text_input("Peso"), c2.text_input("Talla"), c3.text_input("P. Craneano")
        pe, te, pt = c1.text_input("P/E"), c2.text_input("T/E"), c3.text_input("P/T")
        diag = st.text_area("Diagnóstico Nutricional")

    with tab4:
        ind = st.text_area("Acuerdos e Indicaciones")
        der = st.text_area("Derivaciones")
    
    submit = st.form_submit_button("🚀 GENERAR REGISTRO CLÍNICO")

if submit:
    if not nombre:
        st.error("Escriba el nombre del paciente.")
    else:
        datos = {
            "nombre": nombre, "edad": edad, "domicilio": domicilio, "interno": interno,
            "tipo_alim": tipo_alim, "obs_alim": obs_alim, "meds": meds, "examenes": examenes,
            "inst": inst, "peso": peso, "talla": talla, "pc": pc, "pe": pe, "te": te,
            "pt": pt, "diag": diag, "ind": ind, "der": der
        }
        try:
            pdf_bytes = generar_pdf_integral(datos)
            st.success("✅ Registro generado correctamente")
            st.download_button(
                label="📥 DESCARGAR INFORME PDF",
                data=bytes(pdf_bytes),
                file_name=f"Registro_{nombre.replace(' ','_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error: {e}")

# Créditos al final de la pantalla
st.write("---")
st.caption("Sistema generado por el Centro de Habilidades Clínicas y Disciplinares - Universidad de O'Higgins")
