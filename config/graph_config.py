from typing import List, Dict, Any
import streamlit as st
import uuid

from dto.log_entry import LogEntry
from app.graph import run_pipeline


@st.cache_data(show_spinner=False)
def run_analyze_graph(logs: List[LogEntry]) -> Dict[str, Any]:
    request_id = f"graph-{str(uuid.uuid4())}"
    response = run_pipeline(logs_input=logs, request_id=request_id, source="graph")

    return {
        "request_id": response.get("request_id"),
        "received": len(logs),
        "threat_detected": any(a == 1 for a in response.get("predictions", [])),
        "suggested_action": response.get("decision"),
        "report": response.get("report_summary"),
        "reasons": response.get("decision_reasons"),
        "decision_llm": response.get("decision_llm")
    }
