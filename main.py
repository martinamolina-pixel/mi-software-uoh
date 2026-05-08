import streamlit as st
from fpdf import FPDF
import os

# 1. Configuración de página
st.set_page_config(page_title="Registro Clínico UOH", page_icon="🏥", layout="centered")

# --- MANEJO DEL LOGO (Nombre exacto de tu GitHub) ---
nombre_logo = "UOH - EsSa Azul (1) (3) (1).png"

if os.path.exists(nombre_logo):
    st.image(nombre_logo, width=350)
else:
    st.title("🏥 FICHA CLÍNICA UOH")

st.write("---")

# --- CLASE PARA EL REPORTE PDF ---
class PDF(FPDF):
    def header(self):
        if os.path.exists(nombre_logo):
            self.image(nombre_logo, 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'REGISTRO CLÍNICO APS', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Sistema generado por el Centro de Habilidades Clínicas y Disciplinares - UOH', 0, 0, 'C')

# --- FORMULARIO CON PESTAÑAS ---
with st.form("uoh_clinico_final"):
    # Estructura por segmentos solicitada
    t1, t2, t3, t4 = st.tabs(["👤 Identificación", "🩺 Clínica", "📊 Antropometría", "📝 Cierre"])

    with t1:
        nombre = st.text_input("Nombre del Paciente")
        c1, c2 = st.columns(2)
        edad = c1.text_input("Edad")
        domicilio = c2.text_input("Domicilio")
        interno = st.text_input("Interno(a) Responsable")

    with t2:
        tipo_alim = st.selectbox("Tipo de Alimentación", ["LME", "LA", "LM+LA", "Complementaria"])
        obs_alim = st.text_area("Observaciones Alimentación")
        meds = st.text_area("Medicamentos / Suplementos")
        examenes = st.text_area("Vacunas / Exámenes")

    with t3:
        ca, cb, cc = st.columns(3)
        peso, talla, pc = ca.text_input("Peso"), cb.text_input("Talla"), cc.text_input("PC")
        pe, te, pt = ca.text_input("P/E"), cb.text_input("T/E"), cc.text_input("P/T")
        diag = st.text_area("Diagnóstico Nutricional")

    with t4:
        indicaciones = st.text_area("Acuerdos e Indicaciones")
        derivaciones = st.text_area("Derivaciones")

    # Botón dentro del formulario para evitar errores
    enviar = st.form_submit_button("🚀 GENERAR REGISTRO CLÍNICO")

# --- GENERACIÓN DEL PDF (Solución al error 'encode') ---
if enviar:
    if not nombre:
        st.warning("⚠️ Debes ingresar el nombre del paciente.")
    else:
        try:
            pdf = PDF()
            pdf.add_page()
            
            def sec(titulo, contenido):
                pdf.set_font("Arial", 'B', 11)
                pdf.set_fill_color(240, 240, 240)
                pdf.cell(0, 8, titulo, 1, 1, 'L', fill=True)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 7, str(contenido), 1)
                pdf.ln(4)

            sec("I. IDENTIFICACIÓN", f"Paciente: {nombre}\nEdad: {edad}\nInterno: {interno}")
            sec("II. CLÍNICA", f"Alimentación: {tipo_alim}\nObservaciones: {obs_alim}\nMedicamentos: {meds}")
            sec("III. ANTROPOMETRÍA", f"P: {peso} | T: {talla} | PC: {pc}\nIndicadores: {pe}, {te}, {pt}\nDiag: {diag}")
            sec("IV. PLAN", f"Indicaciones: {indicaciones}\nDerivaciones: {derivaciones}")

            # SOLUCIÓN AL ERROR: Convertimos directamente a bytes
            pdf_bytes = pdf.output() 
            
            st.success("✅ Ficha lista para descarga")
            st.download_button(
                label="📥 DESCARGAR REGISTRO PDF",
                data=bytes(pdf_bytes), # Aquí se soluciona el error de la captura
                file_name=f"Registro_{nombre}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error técnico: {e}")

# Créditos institucionales finales
st.write("---")
st.caption("Sistema generado por el Centro de Habilidades Clínicas y Disciplinares - Universidad de O'Higgins")
