import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Configuración de la aplicación
st.set_page_config(page_title="Ficha Clínica UOH", page_icon="🏥")

st.title("🏥 FICHA CLÍNICA UOH")
st.write("Internado APS - Martina Molina")

# --- FUNCIÓN DE GENERACIÓN DE PDF CORREGIDA ---
def generar_pdf(info):
    pdf = FPDF()
    pdf.add_page()
    
    # Título principal
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "FICHA DE ATENCIÓN CLÍNICA", ln=True, align="C")
    pdf.ln(10)
    
    # Contenido
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Detalles del Paciente:", ln=True)
    pdf.set_font("Arial", "", 12)
    
    # Escribimos cada dato asegurando que el texto se ajuste (multi_cell)
    for clave, valor in info.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(40, 10, f"{clave}: ", ln=0)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, f"{valor}")
        pdf.ln(2)
    
    pdf.ln(20)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "__________________________", ln=True, align="C")
    pdf.cell(0, 10, "Firma Interno(a)", ln=True, align="C")
    
    # Salida segura para Streamlit
    return pdf.output()

# --- FORMULARIO DE ENTRADA ---
with st.form("mi_formulario", clear_on_submit=False):
    nombre = st.text_input("Nombre del Paciente")
    edad = st.text_input("Edad")
    diagnostico = st.text_area("Diagnóstico Nutricional")
    acuerdos = st.text_area("Indicaciones y Acuerdos")
    
    boton_preparar = st.form_submit_button("📋 GENERAR FICHA PDF")

if boton_preparar:
    if not nombre:
        st.error("⚠️ Por favor, ingresa el nombre del paciente.")
    else:
        # Preparamos la información
        datos = {
            "Fecha": datetime.now().strftime("%d/%m/%Y"),
            "Paciente": nombre,
            "Edad": edad,
            "Diagnóstico": diagnostico,
            "Acuerdos": acuerdos
        }
        
        try:
            # Generamos los bytes del PDF
            pdf_bytes = generar_pdf(datos)
            
            st.success(f"✅ PDF de {nombre} listo para descargar")
            
            # Botón de descarga con datos ya listos
            st.download_button(
                label="📥 DESCARGAR AHORA",
                data=bytes(pdf_bytes),
                file_name=f"Ficha_{nombre.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Hubo un problema al crear el archivo: {e}")
