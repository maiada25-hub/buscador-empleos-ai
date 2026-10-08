import streamlit as st
import pandas as pd
import os
from datetime import datetime
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Job Tracker AI", page_icon="💼", layout="wide")
st.title("💼 Panel de Búsqueda de Empleo con IA")

# Barra lateral para la configuración de la API
st.sidebar.header("⚙️ Configuración")
st.sidebar.write("Obtén tu clave en [Google AI Studio](https://aistudio.google.com/)")
api_key = st.sidebar.text_input("Clave de API (Gemini)", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Se recomienda usar flash para tareas rápidas de extracción de texto
    modelo = genai.GenerativeModel('gemini-2.5-flash')

ARCHIVO_DATOS = "registro_empleos.csv"

def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        return pd.read_csv(ARCHIVO_DATOS)
    else:
        return pd.DataFrame(columns=["Fecha", "Empresa", "Puesto", "Modalidad", "Estado", "Enlace"])

def guardar_datos(df):
    df.to_csv(ARCHIVO_DATOS, index=False)

df_empleos = cargar_datos()

tab1, tab2 = st.tabs(["📊 Rastreador de Postulaciones", "🤖 Analizador de Ofertas (IA)"])

with tab1:
    st.subheader("Registrar nueva postulación")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        empresa = st.text_input("Empresa")
        puesto = st.text_input("Puesto (ej. Analista de Datos, AI Prompt Engineer)")
    with col2:
        modalidad = st.selectbox("Modalidad", ["Remoto", "Híbrido", "Presencial"])
        estado = st.selectbox("Estado", ["Enviado", "Entrevista", "Prueba Técnica", "Rechazado", "Oferta"])
    with col3:
        enlace = st.text_input("Enlace a la oferta")
        fecha = datetime.today().strftime('%Y-%m-%d')
        
    if st.button("Guardar Postulación"):
        if empresa and puesto:
            nueva_fila = pd.DataFrame([{
                "Fecha": fecha, "Empresa": empresa, "Puesto": puesto, 
                "Modalidad": modalidad, "Estado": estado, "Enlace": enlace
            }])
            df_empleos = pd.concat([df_empleos, nueva_fila], ignore_index=True)
            guardar_datos(df_empleos)
            st.success("¡Postulación guardada con éxito!")
            st.rerun()
        else:
            st.warning("Por favor, rellena al menos la empresa y el puesto.")

    st.divider()
    st.subheader("Tus Postulaciones Activas")
    st.dataframe(df_empleos, use_container_width=True)

with tab2:
    st.subheader("Analizar Descripción de la Oferta")
    st.write("Pega la descripción del trabajo para extraer los requisitos técnicos y habilidades clave.")
    
    descripcion_oferta = st.text_area("Descripción de la oferta de empleo", height=200)
    
    if st.button("Analizar con Google AI"):
        if not api_key:
            st.error("⚠️ Por favor, introduce tu clave de API en la barra lateral primero.")
        elif not descripcion_oferta:
            st.warning("⚠️ Pega una descripción para comenzar.")
        else:
            with st.spinner("Analizando los requisitos..."):
                try:
                    prompt = f"""
                    Actúa como un analista de reclutamiento técnico. Analiza la siguiente descripción de una oferta de empleo y extrae la información en el siguiente formato Markdown:
                    
                    * **Rol/Título:** (El puesto principal)
                    * **Requisitos Técnicos (Hard Skills):** (Lista de herramientas, software, o conocimientos específicos)
                    * **Habilidades Blandas (Soft Skills):** (Capacidades interpersonales o metodológicas)
                    * **Resumen:** (1 frase sobre el objetivo principal del puesto)
                    
                    Descripción de la oferta:
                    {descripcion_oferta}
                    """
                    respuesta = modelo.generate_content(prompt)
                    
                    st.success("Análisis completado:")
                    st.markdown(respuesta.text)
                    
                except Exception as e:
                    st.error(f"Error al conectar con la API: {e}")