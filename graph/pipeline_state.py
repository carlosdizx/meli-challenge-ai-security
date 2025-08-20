from operator import add, or_
from typing import TypedDict, List, Dict, Any, Annotated

from dto.log_entry import LogEntry


class PipelineState(TypedDict, total=False):
    # ---- Entrada y metadatos ----
    request_id: str
    logs_input: list[LogEntry]
    source: str

    # ---- Agente: ingestación (validación) ----
    validated_logs: List[Dict[str, Any]]

    # ---- Agente: transformación ----
    df_raw: Any
    df_transformed: Any
    batch: List[Dict[str, float]]

    # ---- Agente: predict ----
    predictions: List[int]
    scores: List[float]

    # ---- Agente: decisión ----
    decision: str
    decision_reasons: List[str]

    # ---- Agente: reporte ----
    report_df: Any
    report_summary: Dict[str, Any]

    # ---- Acumuladores y misc ----
    errors: Annotated[List[str], add]
    warnings: Annotated[List[str], add]
    meta: Annotated[Dict[str, Any], or_]


def make_initial_state(
        logs_input: List[Dict[str, Any]],
        request_id: str,
        source: str = "api",
) -> PipelineState:
    return {
        "request_id": request_id,
        "source": source,
        "logs_input": logs_input,
        "errors": [],
        "warnings": [],
        "meta": {},
    }
