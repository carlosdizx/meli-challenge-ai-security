from typing import List, Dict, Any, Tuple
import json
import pandas as pd
import streamlit as st

from dto.log_entry import LogEntry


def render_uploader(limit: int) -> Tuple[List[Dict[str, Any]], int]:
    payload: List[Dict[str, Any]] = []
    total = 0

    tab_file, tab_text = st.tabs(["📁 Subir JSON", "✍️ Pegar JSON"])

    with tab_file:
        uploaded = st.file_uploader("Archivo JSON (array de objetos)", type=["json"])
        if uploaded:
            try:
                data = json.load(uploaded)
                if not isinstance(data, list):
                    st.error("El archivo debe contener un **array** JSON.")
                else:
                    LogEntry.parse_list(data)
                    total = len(data)
                    payload = data[:limit]
                    st.success(f"Registros cargados: {len(payload)} / {total}")
                    st.dataframe(pd.json_normalize(payload)[:200])
            except Exception as e:
                st.error(f"No se pudo leer el JSON: {e}")

    with tab_text:
        txt = st.text_area("Pega aquí un array JSON", height=180,
                           placeholder='[{"ip_address":"8.8.8.8","country":"CO",...}]')
        if txt.strip():
            try:
                data = json.loads(txt)
                if not isinstance(data, list):
                    st.error("El contenido debe ser un **array** JSON.")
                else:
                    total = len(data)
                    payload = data[:limit]
                    st.success(f"Registros preparados: {len(payload)} / {total}")
                    st.dataframe(pd.json_normalize(payload)[:200])
            except Exception as e:
                st.error(f"JSON inválido: {e}")

    return payload, total
