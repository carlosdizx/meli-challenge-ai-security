import uuid

from agents.decision import decide
from agents.ingestion import ingest
from agents.report import build_report
from agents.transform import transform
from graph.pipeline_state import make_initial_state
from services.model_service import model_service
from dto.log_entry import LogEntry
from fastapi import APIRouter, HTTPException
from agents.predict import predict

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
    state = make_initial_state(logs_input=logs, request_id=f"api-{str(uuid.uuid4())}")
    state = ingest(state)

    try:
        state = transform(state)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    state = predict(state)

    state = decide(state)

    state = build_report(state)

    anomalies = state["predictions"]
    scores = state["scores"]
    action = state["decision"]
    report = state["report_summary"]

    results = []
    for i, (a, s) in enumerate(zip(anomalies, scores)):
        results.append({
            "index": i,
            "anomaly": a,
            "threat": bool(a),
            "score": s,
            "suggested_action": "alert" if a == 1 else "allow",
            "reasons": ["IsolationForest: outlier"] if a == 1 else []
        })

    return {
        "received": len(logs),
        "threat_detected": any(a == 1 for a in anomalies),
        "suggested_action": action,
        "report": report,
        "results": results
    }
