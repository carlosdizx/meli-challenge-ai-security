import pandas as pd

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


def prepare_batch(state: PipelineState) -> PipelineState:
    logs = state['logs_input']

    df = pd.DataFrame([log.to_dict() for log in logs])

    df['user_agent_string'], _ = pd.factorize(df['user_agent_string'])
    df['browser_name_and_version'], _ = pd.factorize(df['browser_name_and_version'])
    df['os_name_and_version'], _ = pd.factorize(df['os_name_and_version'])
    df['country'], _ = pd.factorize(df['country'])
    df['device_type'], _ = pd.factorize(df['device_type'])

    batch = []
    for i, row in df.iterrows():
        item = {}
        for attr, col_name in FEATURE_KEYMAP.items():
            item[col_name] = float(row[attr])
        batch.append(item)
    state['validated_logs'] = batch

    return state
