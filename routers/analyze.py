import uuid

from fastapi import APIRouter, HTTPException

from app.graph import run_pipeline
from dto.log_entry import LogEntry
from services.model_service import model_service

if not model_service.is_loaded():
    raise HTTPException(status_code=500, detail="Modelo no cargado")

router = APIRouter()


@router.post("/")
def analyze(logs: list[LogEntry]):
    response = run_pipeline(logs_input=logs, request_id=f"api-{str(uuid.uuid4())}", source="api")

    return {
        "request_id": response.get("request_id"),
        "received": len(logs),
        "threat_detected": any(a == 1 for a in response.get("predictions")),
        "suggested_action": response.get("decision"),
        "report": response.get("report_summary"),
        "reasons": response.get("decision_reasons"),
    }
