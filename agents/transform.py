from typing import Dict, List

import pandas as pd

from graph.pipeline_state import PipelineState

CATEGORICAL = [
    "user_agent_string",
    "browser_name_and_version",
    "os_name_and_version",
    "country",
    "device_type",
]

FEATURE_KEYMAP: Dict[str, str] = {
    "country": "Country",
    "asn": "ASN",
    "user_agent_string": "User Agent String",
    "browser_name_and_version": "Browser Name and Version",
    "os_name_and_version": "OS Name and Version",
    "device_type": "Device Type",
    "login_successful": "Login Successful",
}


def transform(state: PipelineState) -> PipelineState:
    if "df_raw" not in state:
        raise ValueError("transform: falta df_raw en el estado; ejecuta primero ingestion")

    df = state["df_raw"].copy()

    for col in CATEGORICAL:
        if col in df.columns:
            codes, _ = pd.factorize(df[col], sort=False)
            df[col] = codes

    batch: List[Dict[str, float]] = []
    for _, row in df.iterrows():
        item: Dict[str, float] = {}
        for attr, col_name in FEATURE_KEYMAP.items():
            v = row[attr]
            try:
                item[col_name] = float(v)
            except Exception:
                raise ValueError(f"Campo '{attr}' debe ser numérico. Valor recibido: {v!r}")
        batch.append(item)

    state["df_transformed"] = df
    state["batch"] = batch
    return state
