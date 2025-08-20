from fastapi import APIRouter, HTTPException
import pandas as pd

from app.services.model_service import model_service
from dto.log_entry import LogEntry

if not model_service.is_loaded():
    raise HTTPException(status_code=500, detail="Modelo no cargado")

router = APIRouter()

FEATURE_KEYMAP = {
    "country": "Country",
    "asn": "ASN",
    "user_agent_string": "User Agent String",
    "browser_name_and_version": "Browser Name and Version",
    "os_name_and_version": "OS Name and Version",
    "device_type": "Device Type",
    "login_successful": "Login Successful",
}


@router.post("/")
def analyze(logs: list[LogEntry]):
    df = pd.DataFrame([log.to_dict() for log in logs])

    df['user_agent_string'], _ = pd.factorize(df['user_agent_string'])
    df['browser_name_and_version'], _ = pd.factorize(df['browser_name_and_version'])
    df['os_name_and_version'], _ = pd.factorize(df['os_name_and_version'])
    df['country'], _ = pd.factorize(df['country'])
    df['device_type'], _ = pd.factorize(df['device_type'])

    try:
        return log_dicts
    except Exception as e:
        print(e)
        raise e
    batch = []
    for i, row in df.iterrows():
        item = {}
        for attr, col_name in FEATURE_KEYMAP.items():
            item[col_name] = float(row[attr])
        batch.append(item)

    anomalies, scores = model_service.predict(batch)
