import streamlit as st
from fpdf import FPDF
import os

# 1. Configuración de página
st.set_page_config(page_title="Registro Clínico UOH", page_icon="🏥", layout="centered")

# --- MOSTRAR LOGO (Ya verificado que funciona) ---
nombre_logo = "UOH - EsSa Azul (1) (3) (1).png"
if os.path.exists(nombre_logo):
    st.image(nombre_logo, width=350)
else:
    st.title("🏥 FICHA CLÍNICA UOH")

st.write("---")

# --- CLASE PARA EL PDF ---
class PDF(FPDF):
    def header(self):
        nombre_logo = "UOH - EsSa Azul (1) (3) (1).png"
        if os.path.exists(nombre_logo):
            self.image(nombre_logo, 10, 8, 33)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'REGISTRO CLÍNICO APS', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Sistema generado por el Centro de Habilidades Clínicas y Disciplinares - UOH', 0, 0, 'C')

# --- FORMULARIO PRINCIPAL ---
# Todo debe estar dentro de este bloque 'with st.form'
with st.form("mi_formulario_clinico"):
    t1, t2, t3, t4 = st.tabs(["👤 Identificación", "🩺 Clínica", "📊 Antropometría", "📝 Cierre"])

    with t1:
        nombre = st.text_input("Nombre del Paciente")
        col1, col2 = st.columns(2)
        edad = col1.text_input("Edad")
        domicilio = col2.text_input("Domicilio")
        interno = st.text_input("Interno(a) Responsable")

    with t2:
        tipo_alim = st.selectbox("Tipo de Alimentación", ["LME", "LA", "LM+LA", "Complementaria"])
        obs_alim = st.text_area("Observaciones Alimentación")
        meds = st.text_area("Medicamentos / Suplementos")
        examenes = st.text_area("Vacunas / Exámenes")

    with t3:
        ca, cb, cc = st.columns(3)
        peso = ca.text_input("Peso (kg)")
        talla = cb.text_input("Talla (cm)")
        pc = cc.text_input("PC")
        pe = ca.text_input("P/E")
        te = cb.text_input("T/E")
        pt = cc.text_input("P/T")
        diag = st.text_area("Diagnóstico Nutricional")

    with t4:
        indicaciones = st.text_area("Acuerdos e Indicaciones")
        derivaciones = st.text_area("Derivaciones")

    # EL BOTÓN DEBE ESTAR AQUÍ ADENTRO (Sangrado a la derecha)
    enviar = st.form_submit_button("🚀 GENERAR REGISTRO CLÍNICO")

# --- LÓGICA DE GENERACIÓN (Fuera del formulario) ---
if enviar:
    if not nombre:
        st.error("Por favor, ingresa el nombre del paciente.")
    else:
        try:
            pdf = PDF()
            pdf.add_page()
            
            def agregar_bloque(titulo, contenido):
                pdf.set_font("Arial", 'B', 11)
                pdf.set_fill_color(240, 240, 240)
                pdf.cell(0, 8, titulo, 1, 1, 'L', fill=True)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(0, 7, str(contenido), 1)
                pdf.ln(4)

            agregar_bloque("I. IDENTIFICACIÓN", f"Paciente: {nombre}\nEdad: {edad}\nInterno: {interno}")
            agregar_bloque("II. CLÍNICA", f"Alimentación: {tipo_alim}\nObservaciones: {obs_alim}\nMedicamentos: {meds}")
            agregar_bloque("III. ANTROPOMETRÍA", f"Peso: {peso} | Talla: {talla} | PC: {pc}\nIndicadores: {pe}, {te}, {pt}\nDiag: {diag}")
            agregar_bloque("IV. PLAN", f"Indicaciones: {indicaciones}\nDerivaciones: {derivaciones}")

            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.success("✅ ¡Ficha generada correctamente!")
            st.download_button(
                label="📥 DESCARGAR REGISTRO PDF",
                data=pdf_output,
                file_name=f"Registro_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error al generar PDF: {e}")

# Créditos finales
st.write("---")
st.caption("Sistema generado por el Centro de Habilidades Clínicas y Disciplinares - Universidad de O'Higgins")
