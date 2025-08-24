# 1. Importar librerias
import pandas as pd
from pathlib import Path


# 2. Transformación de datos, strings a numéricos
def export_csv(df: pd.DataFrame, filename: str, is_validation: bool):
    df['Device Type'] = df['Device Type'].fillna('unknown')

    df['User Agent String'], _ = pd.factorize(df['User Agent String'])
    df['Browser Name and Version'], _ = pd.factorize(df['Browser Name and Version'])
    df['OS Name and Version'], _ = pd.factorize(df['OS Name and Version'])

    categorical_cols = df.select_dtypes(include=['object']).columns

    if not is_validation:
        df.drop(columns=['Is Attack IP'], inplace=True)

    for col in categorical_cols:
        df[col] = df[col].astype('category')
        df[col] = df[col].cat.codes

    # 4. Exportar el dataset transformado a un archivo CSV
    output_path = Path(__file__).parent.parent / 'data' / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset transformado exportado exitosamente a: {output_path}")
