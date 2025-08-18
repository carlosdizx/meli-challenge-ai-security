from fastapi import FastAPI
import pandas as pd
import joblib
from dto.log_entry import LogEntry
from pathlib import Path
from utils.model_loader import ModelManager

app = FastAPI()

model = joblib.load(Path(__file__).parent.parent / 'model/isolation_forest.pkl')

model_manager = ModelManager()

model_manager.load_model('isolation_forest')


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/analyze")
def analyze(logs: list[LogEntry]):
    try:
        log_dicts = [log.to_dict() for log in logs]

        return log_dicts
    except Exception as e:
        print(e)
        raise
