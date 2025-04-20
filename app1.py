import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Pronóstico de Venta", layout="centered")

st.markdown("<h1 style='color:#FF4B4B; text-align:center;'>📊 Pronóstico de Venta</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:#333;'>Ingrese la venta promedio diaria de cada artículo (últimas 3 semanas):</h4>", unsafe_allow_html=True)

articulos = {
    "45955 Pollo rostizado": 0,
    "292524 Milanesa de pollo": 0,
    "39486 Pechuga sin hueso": 0,
    "123988 Ala adobada (15 días)": 0,
    "148377 Muslo sin hueso": 0,
    "39481 Pechuga con hueso": 0,
    "39480 Pollo entero": 0,
}

col1, col2 = st.columns(2)
ventas = {}

for idx, (nombre, _) in enumerate(articulos.items()):
    with (col1 if idx % 2 == 0 else col2):
        ventas[nombre] = st.number_input(f"{nombre}", min_value=0.0, step=0.1)

st.markdown("---")

# Selección de día de pedido
dia_hoy = datetime.today().strftime('%A')
st.markdown(f"<h5 style='color:#666;'>Hoy es: <b>{dia_hoy}</b></h5>", unsafe_allow_html=True)

pedido = st.selectbox("¿Qué día se realizará el pedido?", ["Lunes", "Jueves", "Sábado"])

# Definir días de llegada según pedido
llegadas = {"Lunes": "Viernes", "Jueves": "Lunes", "Sábado": "Miércoles"}
dias_entre = {"Lunes": 4, "Jueves": 4, "Sábado": 4}  # Ajustable si cambia la logística

dias_a_calcular = dias_entre[pedido]

# Cálculo de pronóstico
st.markdown(f"<h4 style='color:#4CAF50;'>🟢 Pronóstico de Venta hasta el siguiente embarque ({dias_a_calcular} días):</h4>", unsafe_allow_html=True)

df = pd.DataFrame(columns=["Artículo", "Venta Prom. Diaria", "Pronóstico"])

for nombre, promedio in ventas.items():
    caducidad = 15 if "Ala adobada" in nombre else 8
    dias_validos = min(dias_a_calcular, caducidad)
    pronostico = round(promedio * dias_validos, 2)
    df.loc[len(df)] = [nombre, promedio, pronostico]

st.dataframe(df, use_container_width=True)

st.markdown("<small style='color:gray;'>* Los productos con caducidad de 8 días se limitan a ese número, incluso si el pedido cubre más días.</small>", unsafe_allow_html=True)
