import pandas as pd

from dto.log_entry import LogEntry
from graph.pipeline_state import PipelineState


def ingest(state: PipelineState) -> PipelineState:
    logs: list[LogEntry] = state["logs_input"]
    validated_logs = [log.to_dict() for log in logs]
    df_raw = pd.DataFrame(validated_logs)

    state["validated_logs"] = validated_logs
    state["df_raw"] = df_raw
    return state
