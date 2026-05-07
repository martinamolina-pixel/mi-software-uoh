import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("🏥 FICHA CLÍNICA UOH")

with st.form("mi_formulario"):
    nombre = st.text_input("Nombre Paciente")
    edad = st.text_input("Edad")
    diag = st.text_input("Diagnóstico")
    boton = st.form_submit_button("💾 GUARDAR EN EXCEL")

if boton:
    if not nombre:
        st.warning("Completa el nombre")
    else:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            # Creamos el dato
            df = pd.DataFrame([{"Fecha": "07-05-2024", "Paciente": nombre, "Edad": edad, "Diagnostico": diag}])
            
            # El comando 'append' es más seguro para no borrar lo anterior
            conn.create(data=df) 
            
            st.balloons()
            st.success(f"¡Éxito! {nombre} registrado.")
        except Exception as e:
            st.error(f"Error de permisos: Asegúrate de que el Excel esté en modo 'Editor' para todos.")
