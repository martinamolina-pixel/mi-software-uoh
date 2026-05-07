# --- LÓGICA DE GUARDADO DEFINITIVA ---
if st.button("💾 GUARDAR REGISTRO CLÍNICO"):
    if nombre_paciente == "":
        st.error("Por favor, ingresa el nombre del paciente.")
    else:
        try:
            # Limpiar cualquier error de conexión previo
            st.cache_resource.clear()
            
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # Preparamos la fila con los nombres de tus columnas actuales
            nuevo_registro = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Paciente": nombre_paciente,
                "Edad": edad,
                "Interno": interno,
                "Peso": peso,
                "Talla": talla,
                "Diagnostico": diag_nutricional
            }])

            # IMPORTANTE: Aquí decimos que la hoja se llama "Datos"
            conn.create(data=nuevo_registro, worksheet="Datos")

            st.balloons()
            st.success(f"¡Registro de {nombre_paciente} guardado con éxito!")
        except Exception as e:
            st.error(f"Error final: {e}. Revisa que en el Excel la pestaña se llame Datos")
