from sklearn.ensemble import IsolationForest
import pandas as pd
import joblib
from pathlib import Path

df = pd.read_csv(Path(__file__).parent.parent / 'data' / 'dataset.csv')

features = df[['Country', 'Region', 'City', 'Device Type', 'Is Attack IP', 'Is Account Takeover']]

model = IsolationForest(contamination=0.1, random_state=42)

model.fit(features)

output_path = Path(__file__).parent.parent / 'model/isolation_forest_model.pkl'
output_path.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, output_path)

print(f"Modelo entrenado y guardado con éxito en {output_path}.")
