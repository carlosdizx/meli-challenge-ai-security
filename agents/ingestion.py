import pandas as pd

from dto.log_entry import LogEntry
from graph.pipeline_state import PipelineState

FEATURE_KEYMAP = {
    "country": "Country",
    "asn": "ASN",
    "user_agent_string": "User Agent String",
    "browser_name_and_version": "Browser Name and Version",
    "os_name_and_version": "OS Name and Version",
    "device_type": "Device Type",
    "login_successful": "Login Successful",
}


def ingest(state: PipelineState) -> PipelineState:
    logs: list[LogEntry] = state["logs_input"]
    validated_logs = [log.to_dict() for log in logs]
    df_raw = pd.DataFrame(validated_logs)

    state["validated_logs"] = validated_logs
    state["df_raw"] = df_raw
    return state
