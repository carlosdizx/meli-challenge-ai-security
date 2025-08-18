# 1. Importar librerias
import pandas as pd
from kagglehub import dataset_download
import tomli
from pathlib import Path
import ipaddress

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

# 5. Transformación de datos, strings a numéricos

df['IP Address'] = df['IP Address'].apply(lambda x: int(ipaddress.ip_address(x)))
df['Device Type'] = df['Device Type'].fillna('unknown')

df['User Agent String'], _ = pd.factorize(df['User Agent String'])
df['Browser Name and Version'], _ = pd.factorize(df['Browser Name and Version'])
df['OS Name and Version'], _ = pd.factorize(df['OS Name and Version'])

categorical_cols = df.select_dtypes(include=['object']).columns

for col in categorical_cols:
    df[col] = df[col].astype('category')
    df[col] = df[col].cat.codes

# 6.Exportar el dataset limpio a un archivo CSV
output_path = Path(__file__).parent.parent / 'data' / 'dataset.csv'
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"Dataset exportado exitosamente a: {output_path}")
