# 💼 Panel de Búsqueda de Empleo con IA (Job Tracker AI)

Una aplicación web interactiva desarrollada en **Python** con **Streamlit** y la potencia de **Google Gemini (Google AI Studio)** para optimizar la búsqueda de empleo y el análisis de ofertas laborales.

## 🚀 Funcionalidades principales

* **📊 Rastreador de Postulaciones:** Permite registrar de manera organizada las ofertas de empleo a las que postulas (empresa, puesto, modalidad, estado actual y enlace) y visualizar el historial completo.
* **🤖 Analizador de Ofertas con IA:** Utiliza modelos de lenguaje avanzados de Google para procesar descripciones de empleo y extraer automáticamente:
  * Rol o título principal.
  * Requisitos técnicos (*Hard Skills*).
  * Habilidades interpersonales (*Soft Skills*).
  * Un resumen claro del puesto.

## 🛠️ Tecnologías utilizadas

* **Python**
* **Streamlit** (para la interfaz web)
* **Pandas** (para la gestión de datos tabulares)
* **Google Generative AI SDK (`google-generativeai`)**

## ⚙️ Instalación y ejecución local

1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias necesarias ejecutando:
   ```bash
   pip install -r requirements.txt
