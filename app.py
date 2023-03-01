import streamlit as st
import pandas as pd
import altair as alt
import folium

# Leer el archivo CSV
df = pd.read_csv('countries-global-temperature.csv')

# Crear una lista de países únicos
paises_unicos = df['Country Name'].unique()

# Crear una lista de años únicos
anios_unicos = [int(col) for col in df.columns[4:]]

# Agregar un título a la página
st.title('Estadísticas de temperatura por país (1970-2021)')

# Crear elementos de la interfaz de usuario
st.sidebar.title('Opciones de selección')
pais = st.sidebar.selectbox('Selecciona un país', paises_unicos)
inicio = st.sidebar.slider(
    'Selecciona el año de inicio', min(anios_unicos), max(anios_unicos))
fin = st.sidebar.slider('Selecciona el año de fin', inicio, max(anios_unicos))
unidad_temp = st.sidebar.selectbox(
    'Selecciona la unidad de temperatura', ['Celsius', 'Fahrenheit'])
tipo_grafico = st.sidebar.selectbox('Selecciona el tipo de gráfico', [
                                    'Línea', 'Punto', 'Barra'])
ver_tabla = st.sidebar.checkbox('Mostrar tabla de datos')

# Filtrar los datos según las selecciones del usuario
columnas = ['Country Name'] + [str(anio) for anio in range(inicio, fin+1)]
df_filtrado = df.loc[df['Country Name'] == pais, columnas]

# Convertir los datos a formato largo (long format) y tipo fecha
df_filtrado = df_filtrado.melt(
    id_vars=['Country Name'], var_name='Year', value_name='AvgTemperature')
df_filtrado['Year'] = pd.to_datetime(df_filtrado['Year'], format='%Y')

# Convertir la temperatura a la unidad seleccionada por el usuario
if unidad_temp == 'Fahrenheit':
    df_filtrado['AvgTemperature'] = df_filtrado['AvgTemperature'].apply(
        lambda x: (x * 1.8) + 32)

# Crear la gráfica de temperatura
if tipo_grafico == 'Línea':
    chart = alt.Chart(df_filtrado).mark_line().encode(
        x='Year',
        y='AvgTemperature'
    )
elif tipo_grafico == 'Punto':
    chart = alt.Chart(df_filtrado).mark_point().encode(
        x='Year',
        y='AvgTemperature'
    )
else:
    chart = alt.Chart(df_filtrado).mark_bar().encode(
        x='Year',
        y='AvgTemperature'
    )

# Mostrar el título y el texto descriptivo de la gráfica
st.markdown(f'### Temperaturas promedio para {pais} ({inicio}-{fin})')
st.write(
    f'Esta gráfica muestra la evolución de las temperaturas promedio para el país seleccionado en {unidad_temp}.')

# Mostrar la gráfica y la tabla de datos en la interfaz de usuario
st.altair_chart(chart, use_container_width=True)

if ver_tabla:
    # Formatear la fecha en la tabla de datos
    df_filtrado['Year'] = df_filtrado['Year'].dt.strftime('%Y')
    st.subheader(f'Tabla de datos de {pais} ({inicio}-{fin})')
    st.write(df_filtrado[['Year', 'AvgTemperature']])
