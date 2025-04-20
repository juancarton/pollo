import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from fpdf import FPDF
import base64

# Configuración de la página
st.set_page_config(page_title="Pronóstico de Venta", layout="centered")

# 🔐 Autenticación
password = st.text_input("Introduce la contraseña para acceder:", type="password")
if password != "Kabah":
    st.warning("Acceso restringido. Introduce la contraseña correcta para continuar.")
    st.stop()

# 🧾 Encabezado
st.markdown("<h1 style='color:#FF4B4B; text-align:center;'>📊 Pronóstico de Venta</h1>", unsafe_allow_html=True)
st.markdown("Ingrese las ventas semanales en kilos de cada artículo:")

# 📦 Lista de artículos
articulos = [
    "45955 Pollo rostizado",
    "292524 Milanesa de pollo",
    "39486 Pechuga sin hueso",
    "123988 Ala adobada",
    "148377 Muslo sin hueso",
    "39481 Pechuga con hueso",
    "39480 Pollo entero"
]

# Entrada de datos
data = []
for articulo in articulos:
    st.markdown(f"**{articulo}**")
    semana1 = st.number_input(f"Semana 1 (kg) - {articulo}", min_value=0, step=1, key=f"{articulo}_s1")
    semana2 = st.number_input(f"Semana 2 (kg) - {articulo}", min_value=0, step=1, key=f"{articulo}_s2")
    semana3 = st.number_input(f"Semana 3 (kg) - {articulo}", min_value=0, step=1, key=f"{articulo}_s3")
    data.append((articulo, semana1, semana2, semana3))

# Cálculos
df = pd.DataFrame(data, columns=["Artículo", "Semana 1", "Semana 2", "Semana 3"])
df["Promedio Diario (kg)"] = ((df["Semana 1"] + df["Semana 2"] + df["Semana 3"]) / 3) / 7
df["Pronóstico 8 días (kg)"] = (df["Promedio Diario (kg)"] * 8).round(2)
df["Cajas (15 kg)"] = (df["Pronóstico 8 días (kg)"] / 15).apply(lambda x: round(x, 2))

# Mostrar tabla
st.markdown("### 📋 Resultados del Pronóstico")
st.dataframe(df[["Artículo", "Promedio Diario (kg)", "Pronóstico 8 días (kg)", "Cajas (15 kg)"]], use_container_width=True)

# Gráfica
st.markdown("### 📈 Pronóstico Diario para los Próximos 8 Días")
fig, ax = plt.subplots(figsize=(10, 5))
dias = [f"Día {i+1}" for i in range(8)]
for _, row in df.iterrows():
    ax.plot(dias, [round(row["Promedio Diario (kg)"], 2)]*8, label=row["Artículo"])
ax.set_ylabel("Kilos")
ax.set_title("Pronóstico Diario por Artículo")
ax.legend(loc="upper right", fontsize="small")
st.pyplot(fig)

# PDF
st.markdown("### 📄 Descargar Pronóstico en PDF")

def generar_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Pronóstico de Venta", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    for _, row in dataframe.iterrows():
        texto = f"{row['Artículo']}: {row['Pronóstico 8 días (kg)']} kg - {row['Cajas (15 kg)']} cajas"
        pdf.cell(0, 10, texto, ln=True)
    return pdf.output(dest="S").encode("latin1")

pdf_bytes = generar_pdf(df)
b64 = base64.b64encode(pdf_bytes).decode()
href = f'<a href="data:application/pdf;base64,{b64}" download="pronostico_venta.pdf">📥 Descargar PDF</a>'
st.markdown(href, unsafe_allow_html=True)
