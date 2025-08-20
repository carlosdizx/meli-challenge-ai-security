from langgraph.graph import StateGraph, END
from typing import Dict, Any

from graph.pipeline_state import PipelineState, make_initial_state
from agents.decision import decide
from agents.ingestion import ingest
from agents.transform import transform
from agents.predict import predict
from agents.report import build_report


# Cada nodo "envuelve" a tu agente y devuelve SOLO los deltas necesarios (keys nuevas/actualizadas)

def node_ingestion(state: PipelineState) -> Dict[str, Any]:
    st = ingest(state)
    return {"validated_logs": st["validated_logs"], "df_raw": st["df_raw"]}


def node_transform(state: PipelineState) -> Dict[str, Any]:
    st = transform(state)
    return {"df_transformed": st["df_transformed"], "batch": st["batch"]}


def node_predict(state: PipelineState) -> Dict[str, Any]:
    st = predict(state)
    return {"predictions": st["predictions"], "scores": st["scores"]}


def node_decide(state: PipelineState) -> Dict[str, Any]:
    st = decide(state)
    return {"decision": st["decision"], "decision_reasons": st["decision_reasons"]}


def node_report(state: PipelineState) -> Dict[str, Any]:
    st = build_report(state)
    return {"report_summary": st["report_summary"], "report_df": st.get("report_df")}


def build_graph():
    g = StateGraph(PipelineState)
    g.add_node("ingestion", node_ingestion)
    g.add_node("transform", node_transform)
    g.add_node("predict", node_predict)
    g.add_node("decision", node_decide)
    g.add_node("report", node_report)

    g.set_entry_point("ingestion")
    g.add_edge("ingestion", "transform")
    g.add_edge("transform", "predict")
    g.add_edge("predict", "decision")
    g.add_edge("decision", "report")
    g.add_edge("report", END)

    return g.compile()


def run_pipeline(logs_input: list, request_id: str, source: str = "api") -> PipelineState:
    app = build_graph()
    state = make_initial_state(logs_input=logs_input, request_id=request_id, source=source)
    return app.invoke(state)
