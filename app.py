#streamlit run app.py
import pandas as pd
import streamlit as st
import plotly as pl
import datetime

def clean_csv(df):
    """Limpieza extraida del análiosis EDA"""
    df.fillna(0, inplace = True)
    df_clean = df.drop_duplicates()
    return df_clean

df = pd.read_csv('vehicles_us.csv')

df_final = clean_csv(df)

# Creando Aplicación:
st.header("Clase 3 del sprint 7 / Prueba")
st.date_input("Selecciona una fecha para el análisis")
st.dataframe(df)