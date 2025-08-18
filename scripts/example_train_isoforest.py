import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

# --- 1. Datos sintéticos: 1000 normales (N~(0,1)) + 20 anomalías (N~(6,1)) ---
rng = np.random.RandomState(42)
X_normal = rng.normal(loc=0, scale=1, size=(1000, 3))
X_anom   = rng.normal(loc=6, scale=1, size=(20, 3))
X_train  = np.vstack([X_normal, X_anom])

# --- 2. Entrenar IsolationForest ---
model = IsolationForest(
    n_estimators=200,
    contamination=0.02,   # % esperado de anomalías aprox.
    random_state=42
)
model.fit(X_train)

# --- 3. Guardar artefacto preentrenado ---
joblib.dump(model, "model_isoforest.pkl")
print("Modelo guardado en model_isoforest.pkl")
