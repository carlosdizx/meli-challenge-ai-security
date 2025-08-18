# 1. Importar librerias
import pandas as pd
from kagglehub import dataset_download
import tomli
from pathlib import Path
import ipaddress
from scripts.export_to_csv import export_csv
from scripts.export_to_json import export_json

# 2. Leer secrets.toml
secrets_path = Path(__file__).resolve().parents[1] / '.streamlit' / 'secrets.toml'

with open(secrets_path, 'rb') as f:
    secrets = tomli.load(f)

chunk_size = int(secrets["DATASET_CHUNK_SIZE"])


def load_dataset():
    # 3. Descargar y leer el dataset

    path = dataset_download("dasgroup/rba-dataset")

    chunks = []

    for chunk in pd.read_csv(f"{path}/rba-dataset.csv", chunksize=chunk_size):
        chunks.append(chunk)

    df = pd.concat(chunks, axis=0)

    # 4.Limpiar el dataset
    df.drop(columns=['index', 'Round-Trip Time [ms]', "Login Timestamp", "Region", "City"],
            inplace=True)

    # 5. Transformación de ips a enteros

    df['IP Address'] = df['IP Address'].apply(lambda x: int(ipaddress.ip_address(x)))

    print(f"Dataset descargado exitosamente en {path}")

    return df


print(f"Descargando dataset, esto puede tardar unos minutos...")
df = load_dataset()

export_json(df)
export_csv(df)
