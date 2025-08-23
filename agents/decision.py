import tomli
from graph.pipeline_state import PipelineState
from services.gemini_service import GeminiService
from pathlib import Path

client = GeminiService()

secrets_path = Path(__file__).resolve().parents[1] / '.streamlit' / 'secrets.toml'

with open(secrets_path, 'rb') as f:
    secrets = tomli.load(f)

llm = bool(secrets.get("USE_LLM"))


def decide(state: PipelineState) -> PipelineState:
    df_raw = state.get("df_raw")
    preds = state.get("predictions", [])
    scores = state.get("scores", [])

    if df_raw is None:
        raise ValueError("decision: falta df_raw en el estado")
    if not preds or not scores:
        raise ValueError("decision: faltan predictions/scores; ejecuta 'predict' primero")

    reasons = []
    decision = "allow"

    if "is_attack_ip" in df_raw.columns and (df_raw["is_attack_ip"] == 1).any():
        decision = "block"
        reasons.append("Flag de IP de ataque en el payload")

    if decision != "block":
        anom_count = sum(1 for p in preds if p == 1)
        if anom_count > 0:
            decision = "alert"
            reasons.append(f"{anom_count} registro(s) anómalo(s) detectado(s) por IsolationForest")
            min_score = min(scores)
            if min_score < -0.15 or anom_count >= max(3, int(0.2 * len(preds))):
                decision = "block"
                reasons.append(f"Severidad alta (min score {min_score:.3f})")

    if decision == "allow":
        reasons.append("Sin anomalías ni flags activados")

    state["decision"] = decision

    if llm:
        print("Tengo que usar llm")
        state["decision_reasons"] = reasons

        prompt = f"""
            **predictions**: {state["predictions"]}
            **score**: {state["scores"]}
            **decision**: {state["decision"]}
            """

        response = client.get_response(prompt)
    else:
        response = ""

    state["decision_llm"] = response
    return state
