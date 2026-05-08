import streamlit as st
from fpdf import FPDF
import os

# 1. Configuración de página
st.set_page_config(page_title="Registro Clínico UOH", page_icon="🏥", layout="centered")

# --- FUNCIÓN PARA EL LOGO INSTITUCIONAL ---
def mostrar_logo_institucional():
    # Usamos el nombre exacto del archivo que subiste a GitHub
    nombre_logo = "UOH - EsSa Azul (1) (3) (1).png"
    if os.path.exists(nombre_logo):
        st.image(nombre_logo, width=450)
    else:
        st.title("🏥 FICHA CLÍNICA UOH")

mostrar_logo_institucional()
st.write("---")

# --- CLASE PARA EL PDF ---
class PDF(FPDF):
    def header(self):
        nombre_logo = "UOH - EsSa Azul (1) (3) (1).png"
        if os.path.exists(nombre_logo):
            self.image(nombre_logo, 10, 8, 40)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'REGISTRO CLÍNICO APS', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Créditos institucionales solicitados
        self.cell(0, 10, 'Sistema generado por el Centro de Habilidades Clínicas y Disciplinares - UOH', 0, 0, 'C')

# --- ESTRUCTURA POR SEGMENTOS (Pestañas) ---
with st.form("registro_uoh"):
    # Recuperamos la navegación que te acomoda
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
        examenes = st.text_area("Vacunas / Exámenes Vigentes")

    with t3:
        ca, cb, cc = st.columns(3)
        peso = ca.text_input("Peso (kg)")
        talla = cb.text_input("Talla (cm)")
        pc = cc.text_input("P. Craneano")
        pe = ca.text_input("P/E")
        te = cb.text_input("T/E")
        pt = cc.text_input("P/T")
        diag = st.text_area("Diagnóstico Nutricional")

    with t4:
        indicaciones = st.text_area("Acuerdos e Indicaciones")
        derivaciones = st.text_area("Derivaciones / Interconsultas")

    # Botón para procesar
    en
