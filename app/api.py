from fastapi import FastAPI
import pandas as pd
import joblib
from dto.log_entry import LogEntry
from pathlib import Path
from utils.model_loader import ModelManager

app = FastAPI()

model = joblib.load(Path(__file__).parent.parent / 'model/isolation_forest.pkl')

model_manager = ModelManager()

model_manager.load_model('isolation_forest', load_encoders=False)
model_manager.load_model('random_forest')
model_manager.load_model('xgboost')


@app.get("/greeting")
def read_root():
    return {"Hello": "World"}


@app.post("/analyze")
def analyze(logs: list[LogEntry]):
    try:
        log_dicts = [log.to_dict() for log in logs]
        df_logs = pd.DataFrame(log_dicts)

        features = df_logs[['Country', 'Region', 'City', 'Device Type', 'Is Attack IP']]

        features['Country'] = features['Country'].astype('category').cat.codes
        features['Region'] = features['Region'].astype('category').cat.codes
        features['City'] = features['City'].astype('category').cat.codes
        features['Device Type'] = features['Device Type'].astype('category').cat.codes

        predictions = model.predict(features)

        result = {"message": "Análisis completado", "predictions": predictions.tolist()}
        return result
    except Exception as e:
        raise Exception(e)
