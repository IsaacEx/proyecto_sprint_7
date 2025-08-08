import pandas as pd
import streamlit as st
import plotly as pl

def clean_csv(df):
    """Limpieza extraida del análiosis EDA"""
    df.fillna(0, inplace = True)
    df_clean = df.drop_duplicated()
    return df_clean

df = pd.read_csv('proyecto_sprint_7\vehicles_us.csv')

df_final = clean_csv(df)

# Creando Aplicación:
st.heads("Clase 3 del sprint 7 / Prueba streamlit")
st.date_
st.dataframe(df)

#streamlit run app.py