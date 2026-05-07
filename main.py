import streamlit as st

# Título y Logo
st.set_page_config(page_title="Software UOH", page_icon="🏥")
st.title("🏥 Sistema Clínico EsSa-UOH")
st.write("Interna: Martina Molina")

# Las pestañas del software
tab1, tab2 = st.tabs(["Identificación", "Antropometría"])

with tab1:
    nombre = st.text_input("Nombre del Paciente")
    rut = st.text_input("RUT")

with tab2:
    peso = st.number_input("Peso (kg)", min_value=0.0)
    talla = st.number_input("Talla (cm)", min_value=0.0)
    if peso > 0 and talla > 0:
        imc = peso / ((talla/100)**2)
        st.success(f"El IMC calculado es: {imc:.2f}")

if st.button("Guardar Ficha"):
    st.balloons()
    st.write(f"¡Ficha de {nombre} guardada!")
