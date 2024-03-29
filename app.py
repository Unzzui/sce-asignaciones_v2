import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

# ---- Start App

img = "images/oca.jpg"
img1 = "images/oca1.png"

st.set_page_config(page_title="Asignaciones SCE", page_icon=img, layout="wide")
# ---- Web App Title ----

st.markdown(
    """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

st.image(img1, width=250)
st.markdown(
    """
#  Asignaciones SCE 
Esta es una app web creada para facilitar las asignaciones realizadas.
---
"""
)

# # ---- Load CSV ----

@st.cache_data(ttl=60)
def load_csv():
    df = pd.read_csv("data/BD_SCE.csv", sep=";")
    df = df[
        [
            "Número de incidencia",
            "DIRECCION",
            "Observaciones de campo",
            "Supervisor",
            "Centro Operativo",
            "Código TdC",
            "Estado TDC",
            "Municipio",
            "Fecha de Inicio de Ejecución de Trabajo",
            "Fecha de fin",
            "FECHA_ASIGNADA_OCA",
            "ESTADO_OCA",
            "ZONAL",
            "AÑO",
            "ITO_ASIGNADO",
        ]
    ]
    df["FECHA_ASIGNADA_OCA"] = pd.to_datetime(df["FECHA_ASIGNADA_OCA"],origin='1899-12-30', unit='D').dt.strftime('%d-%m-%Y')
    return df

df = load_csv()

# # ---- Sidebar Filters ----

st.sidebar.header("Filtre Aqui:")

year = st.sidebar.multiselect(
    "Seleccione el Año:",
    options=df["AÑO"].unique(),
    default=df["AÑO"].unique(),
)

zonal = st.sidebar.multiselect(
    "Seleccione la Zonal:",
    options=df["ZONAL"].unique(),
    default=df["ZONAL"].unique(),
)
estado = st.sidebar.multiselect(
    "Estado:",
    options=df["ESTADO_OCA"].unique(),
    default=["PENDIENTE"],
)

comuna = st.sidebar.multiselect(
    "Comuna:",
    options=df["Municipio"].unique(),
    default=df["Municipio"].unique(),
)

ito = st.sidebar.multiselect(
    "ITO:",
    options=df["ITO_ASIGNADO"].unique(),
    default=df["ITO_ASIGNADO"].unique(),
)

df_selection = df.query(
    "AÑO == @year & ZONAL == @zonal & ESTADO_OCA == @estado & Municipio == @comuna & ITO_ASIGNADO == @ito"
)

# # ---- Main Page ----

st.title(":memo: Asignaciones Servicio Calidad de Emergencias")
st.markdown("##")

# # ---- Download Button ----

def to_excel(df_selection):
    output = BytesIO()
    df_selection.to_excel(output, index=False, sheet_name='Incidencias')
    processed_data = output.getvalue()
    return processed_data

today = date.today().strftime("%d/%m/%Y")
df_selection_xlsx = to_excel(df_selection)
st.download_button(label='📥 Descargar Excel',
                   data=df_selection_xlsx,
                   file_name='Asignaciones_' + today + '.xlsx')

# # ---- TOP KPIs ----

total_cuenta_pendiente = len(df_selection["ESTADO_OCA"])

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Total Pendientes:")
    st.subheader(total_cuenta_pendiente)

st.write(df_selection)
