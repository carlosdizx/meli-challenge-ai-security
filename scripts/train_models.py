import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, accuracy_score

# Función para exportar CSV (opcional si ya tienes los datasets)
def export_csv(df, filename, index=False):
    path = Path(__file__).parent.parent / 'data' / filename
    df.to_csv(path, index=index)
    print(f"Archivo guardado: {path}")

# --- Cargar datasets ---
data_path = Path(__file__).parent.parent / 'data' / 'dataset.csv'
validation_path = Path(__file__).parent.parent / 'data' / 'validation_dataset.csv'

print(f"Cargando datos de entrenamiento: {data_path}")
print(f"Cargando datos de validación: {validation_path}")

df_train = pd.read_csv(data_path)  # solo features
df_val = pd.read_csv(validation_path)  # features + Is Attack IP

# Separar features y etiquetas de validación
X_val = df_val.drop(columns=["Is Attack IP"])
y_val = df_val["Is Attack IP"]

# --- Entrenamiento ---
print("\nEntrenando Isolation Forest...")

model = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
model.fit(df_train)  # solo features

# --- Evaluación ---
y_pred = model.predict(X_val)
# IsolationForest devuelve -1 para anomalías y 1 para normal
y_pred = [1 if x == -1 else 0 for x in y_pred]

print("\nResultados de Isolation Forest:")
print(classification_report(y_val, y_pred, target_names=['Normal', 'Anomalía'], zero_division=0))
print(f"Precisión: {100 * accuracy_score(y_val, y_pred):.4f}%")

# --- Guardar modelo ---
output_dir = Path(__file__).parent.parent / 'models'
output_dir.mkdir(parents=True, exist_ok=True)
model_path = output_dir / 'isolation_forest_model.pkl'
joblib.dump(model, model_path)
print(f"\nModelo guardado en {model_path}")
