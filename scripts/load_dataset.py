# 1. Importar librerias
import pandas as pd
from kagglehub import dataset_download
import tomli
from pathlib import Path
from scripts.export_to_csv import export_csv
from scripts.export_to_json import export_json
from sklearn.model_selection import train_test_split

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
    df.drop(columns=['index', 'Round-Trip Time [ms]', "Login Timestamp", "Region", "City", "Is Account Takeover",
                     "User ID", 'IP Address'],
            inplace=True)

    df.dropna(inplace=True)

    print(f"Dataset descargado exitosamente en {path}")

    return df


print(f"Descargando dataset, esto puede tardar unos minutos...")
df = load_dataset()

train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

export_csv(train_df, "dataset.csv", False)         # 80%
export_csv(val_df, "validation_dataset.csv", True) # 10%

for i in range(6):
    start_idx = i * 10000
    end_idx = start_idx + 10000
    chunk = test_df.iloc[start_idx:end_idx]
    export_json(chunk, f"chunk_{i + 1}.json")

export_csv(test_df, "test_dataset.csv", False)     # 10