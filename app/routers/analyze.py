import uuid

from agents.ingestion import ingest
from agents.transform import transform
from graph.pipeline_state import make_initial_state
from services.model_service import model_service
from dto.log_entry import LogEntry
from fastapi import APIRouter, HTTPException, Request
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
def analyze(request: Request, logs: list[LogEntry]):
    request_id = request.state.correlation_id if hasattr(request.state, 'correlation_id') else str(uuid.uuid4())
    state = make_initial_state(logs_input=logs, request_id=request_id)
    state = ingest(state)

    try:
        state = transform(state)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    state = predict(state)
    anomalies = state["predictions"]
    scores = state["scores"]

    df_raw = state["df_raw"]
    if "is_attack_ip" in df_raw.columns and (df_raw["is_attack_ip"] == 1).any():
        action = "block"
    elif any(a == 1 for a in anomalies):
        action = "alert"
    else:
        action = "allow"

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
        "results": results
    }
