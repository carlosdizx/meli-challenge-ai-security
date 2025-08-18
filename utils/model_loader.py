from pathlib import Path
import joblib


class ModelManager:
    def __init__(self, model_dir=None):
        self.model_dir = Path(model_dir or Path(__file__).parent.parent / 'model')
        self.models = {}
        self.label_encoders = {}

    def load_model(self, model_name: str):
        model_path = self.model_dir / f"{model_name}.pkl"
        model = joblib.load(model_path)
        self.models[model_name] = model

        return model

    def get_model(self, model_name: str):
        return self.models.get(model_name)