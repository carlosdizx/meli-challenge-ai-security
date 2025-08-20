import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import joblib

MODELS_DIR = Path("models")
MODEL_FILE = MODELS_DIR / "isolation_forest.pkl"
FEATS_FILE = MODELS_DIR / "feature_columns.json"


class ModelService:
    def __init__(self) -> None:
        self.model = None
        self.feature_cols: List[str] = []
        self._load()

    def _load(self) -> None:
        if not MODEL_FILE.exists():
            raise RuntimeError(f"No se encontró el modelo en {MODEL_FILE}")
        if not FEATS_FILE.exists():
            raise RuntimeError(f"No se encontró el archivo de columnas en {FEATS_FILE}")

        self.model = joblib.load(MODEL_FILE)
        with open(FEATS_FILE, "r", encoding="utf-8") as f:
            self.feature_cols = json.load(f)

    def is_loaded(self) -> bool:
        return self.model is not None and len(self.feature_cols) > 0

    def prepare_batch(self, batch: List[Dict[str, Any]]) -> np.ndarray:
        for i, r in enumerate(batch):
            missing = [c for c in self.feature_cols if c not in r]
            if missing:
                raise ValueError(f"Registro {i}: faltan columnas {missing}")
        rows = []
        for r in batch:
            row = []
            for c in self.feature_cols:
                v = r[c]
                try:
                    row.append(float(v))
                except Exception:
                    raise ValueError(f"Columna '{c}' debe ser numérica. Valor recibido: {v}")
            rows.append(row)
        return np.array(rows, dtype=float)

    def predict(self, batch: List[Dict[str, Any]]) -> Tuple[List[int], List[float]]:
        X = self.prepare_batch(batch)
        preds = self.model.predict(X)
        scores = self.model.decision_function(X)
        anomalies = [1 if p == -1 else 0 for p in preds]
        return anomalies, scores.tolist()


model_service = ModelService()
