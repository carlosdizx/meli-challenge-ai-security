import json
from typing import List, Dict, Any

import pandas as pd
import requests
import streamlit as st

# ---------- Sidebar ----------
st.sidebar.title("RBA Anomaly Demo")
base_url = st.sidebar.text_input("API base URL", value="http://127.0.0.1:4200")
endpoint = f"{base_url.rstrip('/')}/analyze/"
limit = st.sidebar.slider("Máximo de registros a enviar", min_value=1, max_value=2000, value=200, step=50)
st.sidebar.caption("La API recibe una lista de logs en snake_case (tu DTO).")

# ---------- Entrada ----------
st.title("Anomaly Detection — RBA Dashboard")
st.write("Sube un JSON (array de objetos) o pega el body.")

tab_file, tab_text = st.tabs(["📁 Subir archivo JSON", "✍️ Pegar JSON"])

payload: List[Dict[str, Any]] = []

with tab_file:
    uploaded = st.file_uploader("Archivo JSON (máx 200MB)",
                                type=["json"])  # límite estándar de Streamlit :contentReference[oaicite:1]{index=1}
    if uploaded:
        try:
            data = json.load(uploaded)
            if not isinstance(data, list):
                st.error("El archivo debe contener un **array** JSON.")
            else:
                payload = data[:limit]
                st.success(f"Registros cargados: {len(payload)} (de {len(data)})")
                st.dataframe(pd.json_normalize(payload)[:200])  # preview
        except Exception as e:
            st.error(f"No se pudo leer el JSON: {e}")

with tab_text:
    txt = st.text_area("Pega aquí un array JSON", height=200, placeholder='[{"ip_address":"8.8.8.8", ...}]')
    if txt.strip():
        try:
            data = json.loads(txt)
            if not isinstance(data, list):
                st.error("El contenido debe ser un **array** JSON.")
            else:
                payload = data[:limit]
                st.success(f"Registros preparados: {len(payload)}")
                st.dataframe(pd.json_normalize(payload)[:200])
        except Exception as e:
            st.error(f"JSON inválido: {e}")


# ---------- Llamada API (cacheable) ----------
@st.cache_data(
    show_spinner=False)  # cachea I/O de datos para evitar recomputar innecesario :contentReference[oaicite:2]{index=2}
def call_api(endpoint: str, body: List[Dict[str, Any]]) -> Dict[str, Any]:
    r = requests.post(endpoint, json=body, timeout=60)
    r.raise_for_status()
    return r.json()


if payload:
    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        run = st.button("Analizar", type="primary")
    with col_btn2:
        st.caption(f"POST → {endpoint}")

    if run:
        try:
            resp = call_api(endpoint, payload)

            # ---------- Métricas ----------
            st.subheader("Resumen")
            m1, m2, m3 = st.columns(3)
            m1.metric("Registros",
                      resp.get("report", {}).get("total", len(payload)))  # :contentReference[oaicite:3]{index=3}
            m2.metric("Anomalías", resp.get("report", {}).get("anomalies", 0))
            m3.metric("Acción sugerida", resp.get("suggested_action", "unknown"))

            # ---------- Gráficos ----------
            report = resp.get("report") or {}
            by_country = report.get("by_country") or []
            by_device = report.get("by_device") or []

            if by_country:
                st.subheader("Tasa de anomalía por país (Top)")
                df_c = pd.DataFrame(by_country)
                st.bar_chart(
                    df_c.set_index("country")["anomaly_rate"])  # gráfico nativo :contentReference[oaicite:4]{index=4}

            if by_device:
                st.subheader("Tasa de anomalía por dispositivo")
                df_d = pd.DataFrame(by_device)
                st.bar_chart(df_d.set_index("device_type")["anomaly_rate"])  # :contentReference[oaicite:5]{index=5}

            # ---------- Casos más severos ----------
            st.subheader("Top casos (score más negativo)")
            top = report.get("top_cases") or []
            if top:
                st.dataframe(pd.DataFrame(top))

            # ---------- Detalle crudo ----------
            with st.expander("Ver respuesta completa"):
                st.json(resp)  # pretty-printed JSON :contentReference[oaicite:6]{index=6}

        except requests.exceptions.RequestException as e:
            st.error(f"Error al llamar la API: {e}")
else:
    st.info("Carga un JSON o pega el body para habilitar el análisis.")
