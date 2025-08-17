from pathlib import Path
import joblib


class ModelManager:
    def __init__(self, model_dir=None):
        self.model_dir = Path(model_dir or Path(__file__).parent.parent / 'model')
        self.models = {}
        self.label_encoders = {}

    def load_model(self, model_name: str, load_encoders=True):
        model_path = self.model_dir / f"{model_name}.pkl"
        model = joblib.load(model_path)
        self.models[model_name] = model

        if load_encoders:
            encoders_path = self.model_dir / f"{model_name}_label_encoders.pkl"
            if encoders_path.exists():
                self.label_encoders[model_name] = joblib.load(encoders_path)
            else:
                self.label_encoders[model_name] = None
        return model

    def get_model(self, model_name: str):
        return self.models.get(model_name)

    def get_label_encoders(self, model_name: str):
        return self.label_encoders.get(model_name)
