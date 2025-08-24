from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import joblib

MODELS_DIR = Path("models")
MODEL_FILE = MODELS_DIR / "isolation_forest_model.pkl"


class ModelService:
    def __init__(self) -> None:
        self.model = None
        self._load()

    def _load(self) -> None:
        if not MODEL_FILE.exists():
            raise RuntimeError(f"No se encontró el modelo en {MODEL_FILE}")
        self.model = joblib.load(MODEL_FILE)
        print(f"Modelo cargado desde {MODEL_FILE}")

    def is_loaded(self) -> bool:
        return self.model is not None

    def prepare_batch(self, batch: List[Dict[str, Any]]) -> np.ndarray:
        # Convertir dicts de features a array de numpy
        rows = []
        for i, r in enumerate(batch):
            row = []
            for k, v in r.items():
                try:
                    row.append(float(v))
                except Exception:
                    raise ValueError(f"Columna '{k}' debe ser numérica. Valor recibido: {v}")
            rows.append(row)
        return np.array(rows, dtype=float)

    def predict(self, batch: List[Dict[str, Any]]) -> Tuple[List[int], List[float]]:
        if not self.is_loaded():
            raise RuntimeError("Modelo no cargado")
        X = self.prepare_batch(batch)
        preds = self.model.predict(X)
        scores = self.model.decision_function(X)
        anomalies = [1 if p == -1 else 0 for p in preds]
        return anomalies, scores.tolist()


model_service = ModelService()
