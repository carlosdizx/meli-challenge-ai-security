from fastapi import APIRouter, HTTPException
import pandas as pd

from app.services.model_service import model_service
from dto.log_entry import LogEntry

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
    log_dicts = [log.to_dict() for log in logs]

    try:
        return log_dicts
    except Exception as e:
        print(e)
        raise e
