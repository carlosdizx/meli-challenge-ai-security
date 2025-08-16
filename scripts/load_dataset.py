# Importar librerias
import pandas as pd
from kagglehub import dataset_download
import streamlit as st

rows = st.secrets["DATASET_ROWS"]


# Descargar y leer el dataset
path = dataset_download("dasgroup/rba-dataset")
df = pd.read_csv(f"{path}/rba-dataset.csv", nrows=rows)