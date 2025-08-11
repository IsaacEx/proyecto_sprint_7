import streamlit as st
import pandas as pd
import plotly.express as px

# --- Carga y Limpieza de Datos ---

# Cargar el archivo CSV
df = pd.read_csv("vehicles_us.csv")

# --- Limpieza simple para despliegue rápido de la app ---
# Rellenar nulos en columnas numéricas clave con medianas (más robusto que media).
# 'odometer' se rellena con la media para no afectar tanto los cálculos.
df["model_year"].fillna(df["model_year"].median(), inplace=True)
df["cylinders"].fillna(df["cylinders"].median(), inplace=True)
df["odometer"].fillna(df["odometer"].mean(), inplace=True)
df["is_4wd"].fillna(0, inplace=True)  # Variable binaria, 0 = no 4wd

# Rellenar nulos en columnas categóricas con valor "desconocido"
df["paint_color"].fillna("desconocido", inplace=True)

# 'date_posted' lo dejamos tal cual o convertirlo a datetime si usas fechas
df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")

# Eliminar filas duplicadas para evitar datos repetidos
df.drop_duplicates(inplace=True)

# --- DataFrame listo para usar sin nulos y sin afectar la calidad ---

# --- Aplicación Web con Streamlit ---

st.set_page_config(layout="wide")
st.header("ANÁLISIS: ANUNCIOS DE VENTA DE COCHES 🚗")
st.write("A través de esta página se puede la información de un conjunto de datos sobre anuncios de vehículos a lo largo de los años.")
st.subheader("Explora los datos de forma interactiva")
st.write("Usa las casillas y filtros para generar gráficos y analizar los datos.")

# Mostrar resumen básico de los datos
st.write(f"**Total de vehículos disponibles:** {len(df)}")
st.write(f"**Años de modelo disponibles:** desde {int(df['model_year'].min())} hasta {int(df['model_year'].max())}")
st.write(f"**Precio promedio:** ${df['price'].mean():,.2f}")

# Filtros interactivos para mejorar el análisis

# Usamos columnas para organizar los filtros y que no se vea todo apilado
col1, col2 = st.columns(2)

with col1:
    # Filtro para el rango de años del modelo
    year_min, year_max = int(df['model_year'].min()), int(df['model_year'].max())
    selected_year_range = st.slider(
        "Selecciona rango de años del modelo",
        min_value=year_min, max_value=year_max,
        value=(year_min, year_max)
    )

with col2:
    # Filtro para el rango de precios
    price_min, price_max = int(df['price'].min()), int(df['price'].max())
    selected_price_range = st.slider(
        "Selecciona rango de precios",
        min_value=price_min, max_value=price_max,
        value=(price_min, price_max)
    )

# Aplicar filtros al DataFrame
df_filtered = df[
    (df['model_year'] >= selected_year_range[0]) & (df['model_year'] <= selected_year_range[1]) &
    (df['price'] >= selected_price_range[0]) & (df['price'] <= selected_price_range[1])
]
##
# Checkbox y código para construir el histograma
build_histogram = st.checkbox("Construir un histograma de odómetro")

if build_histogram:
    st.write("Histograma de la distribución del odómetro de los vehículos")
    fig_hist = px.histogram(
        df_filtered,
        x="odometer",
        title="Distribución del Odómetro",
        labels={"odometer": "Kilometraje (odómetro)", "count": "Cantidad de vehículos"},
        nbins=50,
        template="plotly_white",
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Checkbox y código para construir el gráfico de dispersión
build_scatter = st.checkbox("Construir un gráfico de dispersión de precio vs. año")

if build_scatter:
    st.write("Gráfico de dispersión para ver la relación entre precio y año del modelo")
    fig_scatter = px.scatter(
        df_filtered,
        x="model_year",
        y="price",
        title="Precio vs. Año del Modelo",
        color = "condition",
        opacity = 0.6,
        labels={"model_year": "Año del Modelo", "price": "Precio ($)"},
        template="plotly_white"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


# st.dataframe(df)
# streamlit run app.py
# import datetime
