from graph.pipeline_state import PipelineState
from services.model_service import model_service


def predict(state: PipelineState) -> PipelineState:
    if "batch" not in state or not state["batch"]:
        raise ValueError("predict: falta 'batch' en el estado; ejecuta transform primero")

    anomalies, scores = model_service.predict(state["batch"])
    state["predictions"] = anomalies
    state["scores"] = scores
    return state
