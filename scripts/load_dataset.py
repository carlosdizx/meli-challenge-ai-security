# 1. Importar librerias
import pandas as pd
from kagglehub import dataset_download
import tomli
from pathlib import Path
import ipaddress
from dto.log_entry import LogEntry
import json

# 2. Leer secrets.toml
secrets_path = Path(__file__).parent.parent / '.streamlit' / 'secrets.toml'
with open(secrets_path, 'rb') as f:
    secrets = tomli.load(f)

rows = secrets["DATASET_ROWS"]

# 3. Descargar y leer el dataset
path = dataset_download("dasgroup/rba-dataset")

df = pd.read_csv(f"{path}/rba-dataset.csv", nrows=int(rows))

# 4.Limpiar el dataset
df.drop(columns=['index', 'Round-Trip Time [ms]', "Login Timestamp", "Region", "City"],
        inplace=True)

# 5. Exportar el dataset limpio a un archivo JSON usando la clase LogEntry

df['IP Address'] = df['IP Address'].apply(lambda x: int(ipaddress.ip_address(x)))

records = df.to_dict('records')

log_entries = [LogEntry.from_dict(record).to_dict() for record in records]

output_path = Path(__file__).parent.parent / 'data' / 'dataset.json'
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(log_entries, f, indent=2, ensure_ascii=False)

print(f"Dataset limpio exportado exitosamente a: {output_path}")

# 6. Transformación de datos, strings a numéricos

df['Device Type'] = df['Device Type'].fillna('unknown')

df['User Agent String'], _ = pd.factorize(df['User Agent String'])
df['Browser Name and Version'], _ = pd.factorize(df['Browser Name and Version'])
df['OS Name and Version'], _ = pd.factorize(df['OS Name and Version'])

categorical_cols = df.select_dtypes(include=['object']).columns

for col in categorical_cols:
    df[col] = df[col].astype('category')
    df[col] = df[col].cat.codes

# 7. Exportar el dataset transformado a un archivo CSV
output_path = Path(__file__).parent.parent / 'data' / 'dataset.csv'
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"Dataset transformado exportado exitosamente a: {output_path}")
