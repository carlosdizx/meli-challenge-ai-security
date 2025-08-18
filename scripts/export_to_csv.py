# 1. Importar librerias
import pandas as pd
from pathlib import Path
from scripts.download_dataset import load_dataset

# 2. Leer dataset

df = load_dataset()

# 3. Transformación de datos, strings a numéricos

df['Device Type'] = df['Device Type'].fillna('unknown')

df['User Agent String'], _ = pd.factorize(df['User Agent String'])
df['Browser Name and Version'], _ = pd.factorize(df['Browser Name and Version'])
df['OS Name and Version'], _ = pd.factorize(df['OS Name and Version'])

categorical_cols = df.select_dtypes(include=['object']).columns

for col in categorical_cols:
    df[col] = df[col].astype('category')
    df[col] = df[col].cat.codes

# 4. Exportar el dataset transformado a un archivo CSV
output_path = Path(__file__).parent.parent / 'data' / 'dataset.csv'
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)
print(f"Dataset transformado exportado exitosamente a: {output_path}")
