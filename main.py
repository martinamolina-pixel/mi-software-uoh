import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Ficha Clínica UOH", page_icon="🏥")

st.title("🏥 FICHA CLÍNICA UOH")
st.write("Internado APS - Martina Molina")

# --- FUNCIÓN PARA GENERAR EL PDF ---
def generar_pdf(datos_paciente):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "FICHA DE ATENCIÓN CLÍNICA", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Datos del Paciente:", ln=True)
    pdf.set_font("Arial", "", 12)
    
    for clave, valor in datos_paciente.items():
        pdf.multi_cell(0, 10, f"{clave}: {valor}")
    
    pdf.ln(20)
    pdf.cell(0, 10, "__________________________", ln=True, align="C")
    pdf.cell(0, 10, "Firma Interno(a)", ln=True, align="C")
    
    # Retornar los bytes del PDF
    return pdf.output()

# --- FORMULARIO ---
with st.form("ficha_clinica"):
    nombre = st.text_input("Nombre del Paciente")
    edad = st.text_input("Edad")
    diag = st.text_input("Diagnóstico Nutricional")
    acuerdos = st.text_area("Acuerdos y Derivaciones")
    
    submit = st.form_submit_button("📋 PREPARAR FICHA")

if submit:
    if not nombre:
        st.error("Por favor, ingresa el nombre.")
    else:
        # Creamos un diccionario con la info
        info = {
            "Fecha": datetime.now().strftime("%d/%m/%Y"),
            "Paciente": nombre,
            "Edad": edad,
            "Diagnóstico": diag,
            "Acuerdos": acuerdos
        }
        
        # Generamos el PDF
        pdf_output = generar_pdf(info)
        
        st.success(f"✅ Ficha de {nombre} lista para descargar")
        
        # EL BOTÓN DE DESCARGA: Ahora más simple
        st.download_button(
            label="📥 DESCARGAR PDF",
            data=bytes(pdf_output),
            file_name=f"Ficha_{nombre}.pdf",
            mime="application/pdf"
        )
