import numpy as np
import joblib

# --- 1. Cargar modelo preentrenado ---
model = joblib.load("model_isoforest.pkl")

# --- 2. Lote de registros a evaluar (ejemplo) ---
X_batch = np.array([
    [0.1, -0.2, 0.3],   # probablemente normal
    [6.2, 5.9, 6.1]     # probablemente anomalía
])

# --- 3. Inferencia ---
# predict: 1 = normal, -1 = outlier
labels = model.predict(X_batch)

# decision_function: score (más negativo = más anómalo)
scores = model.decision_function(X_batch)

# Interpretación simple
for i, (lab, sc) in enumerate(zip(labels, scores), start=1):
    print(f"fila {i}: pred={lab}  score={sc:.3f}")
