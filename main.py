import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Ficha Clínica UOH", page_icon="🏥")

st.title("🏥 REGISTRO CLÍNICO UOH")
st.write("Internado APS - Martina Molina")

# --- FUNCIÓN PARA GENERAR EL PDF ---
def crear_pdf(nombre, edad, diag, indicaciones):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "FICHA DE ATENCIÓN CLÍNICA", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="R")
    pdf.ln(10)
    
    # Cuerpo del documento
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Datos del Paciente:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Nombre: {nombre}", ln=True)
    pdf.cell(0, 10, f"Edad: {edad}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Diagnóstico Nutricional:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, diag)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Indicaciones y Acuerdos:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, indicaciones)
    
    # Pie de página (Tu firma)
    pdf.ln(20)
    pdf.cell(0, 10, "__________________________", ln=True, align="C")
    pdf.cell(0, 10, "Interno(a) de Enfermería UOH", ln=True, align="C")
    
    return pdf.output(dest='S')

# --- FORMULARIO ---
with st.form("ficha_clinica"):
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre Completo del Paciente")
        edad = st.text_input("Edad")
    with col2:
        diag = st.text_input("Diagnóstico Nutricional")
    
    indicaciones = st.text_area("Indicaciones, Acuerdos y Derivaciones")
    
    generar = st.form_submit_button("✨ GENERAR FICHA PDF")

if generar:
    if not nombre:
        st.warning("Escribe el nombre del paciente.")
    else:
        # Generar el archivo PDF en memoria
        pdf_bytes = crear_pdf(nombre, edad, diag, indicaciones)
        
        st.balloons()
        st.success(f"Ficha de {nombre} generada correctamente.")
        
        # Botón para descargar el PDF
        st.download_button(
            label="📥 DESCARGAR FICHA EN PDF",
            data=pdf_bytes,
            file_name=f"Ficha_{nombre.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
