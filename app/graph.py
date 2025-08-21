from langgraph.graph import StateGraph, END

from agents.decision import decide
from agents.ingestion import ingest
from agents.transform import transform
from agents.predict import predict
from agents.report import build_report
from graph.pipeline_state import PipelineState, make_initial_state


def node_ingestion(state: PipelineState) -> PipelineState:
    state = ingest(state)
    return state


def node_transform(state: PipelineState) -> PipelineState:
    state = transform(state)
    return state


def node_predict(state: PipelineState) -> PipelineState:
    state = predict(state)
    return state


def node_decide(state: PipelineState) -> PipelineState:
    state = decide(state)
    return state


def node_report(state: PipelineState) -> PipelineState:
    state = build_report(state)
    return state


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
