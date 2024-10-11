import streamlit as st
import pandas as pd
import openai
import speech_recognition as sr
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from langchain import OpenAI
from pandasai import PandasAI

# Configuración de la API de OpenAI
st.sidebar.title("Configuración")
api_key = st.sidebar.text_input("Ingresa tu API de OpenAI")
openai.api_key = api_key

# Inicializar reconocimiento de voz
recognizer = sr.Recognizer()

# Función para cargar y analizar datos
def load_data(uploaded_file, sql_connection):
    if uploaded_file is not None:
        return pd.read_excel(uploaded_file)
    elif sql_connection:
        query = st.sidebar.text_area("Consulta SQL")
        if st.sidebar.button("Ejecutar consulta"):
            engine = create_engine(sql_connection)
            return pd.read_sql(query, engine)
    return None

# Función para análisis de ventas
def analyze_sales(df, products):
    if df is not None and not df.empty:
        analysis = df[df['Product'].isin(products)]
        return analysis.groupby('Product').sum()

# Cargar archivo Excel o datos SQL
uploaded_file = st.sidebar.file_uploader("Sube un archivo Excel", type=["xlsx"])
sql_connection = st.sidebar.text_input("Conexión SQL (URL)")

df = load_data(uploaded_file, sql_connection)

# Interfaz principal
st.title("Bienvenido, soy el agente de NUDELPA LTDA. ¿Qué deseas saber?")

# Campo de entrada de texto
user_input = st.text_input("Pregunta o comando")

# Análisis mediante texto
if user_input and df is not None:
    st.write("Análisis solicitado: ", user_input)
    products = user_input.split(", ")  # Suponiendo que el usuario ingresa productos separados por comas
    analysis_result = analyze_sales(df, products)
    st.write(analysis_result)

# Análisis mediante voz
if st.button("Usar voz"):
    with sr.Microphone() as source:
        st.write("Escuchando...")
        audio = recognizer.listen(source)

        try:
            voice_input = recognizer.recognize_google(audio)
            st.write("Comando recibido: ", voice_input)
            products = voice_input.split(", ")  # Suponiendo que los productos se mencionan en voz
            analysis_result = analyze_sales(df, products)
            st.write(analysis_result)
        except sr.UnknownValueError:
            st.write("No pude entender el audio")
        except sr.RequestError as e:
            st.write(f"Error con el servicio de reconocimiento de voz: {e}")

# Mostrar gráficos
if st.button("Mostrar análisis gráfico"):
    if df is not None:
        plt.figure(figsize=(10, 5))
        plt.plot(df['Date'], df['Sales'], label='Ventas')
        plt.title('Análisis de Ventas')
        plt.xlabel('Fecha')
        plt.ylabel('Ventas')
        plt.legend()
        st.pyplot(plt)
