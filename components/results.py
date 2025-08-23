from typing import Dict, Any
import pandas as pd
import streamlit as st


def render_results(resp: Dict[str, Any]) -> None:
    report = resp.get("report") or {}
    total = report.get("total", 0)
    anomalies = report.get("anomalies", 0)
    action = resp.get("suggested_action", "unknown")
    decision_llm = resp.get("decision_llm", "unknown")

    st.subheader("Resumen")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registros", total)
    c2.metric("Anomalías", anomalies)
    c3.metric("Acción sugerida", action)
    st.markdown(f"**Decision LLM:** {decision_llm}")

    by_country = report.get("by_country") or []
    by_device = report.get("by_device") or []
    top_cases = report.get("top_cases") or []

    if by_country:
        st.subheader("Tasa de anomalía por país (Top)")
        df_c = pd.DataFrame(by_country)
        st.bar_chart(df_c.set_index("country")["anomaly_rate"])

    if by_device:
        st.subheader("Tasa de anomalía por dispositivo")
        df_d = pd.DataFrame(by_device)
        st.bar_chart(df_d.set_index("device_type")["anomaly_rate"])

    st.subheader("Top casos (score más negativo)")
    if top_cases:
        st.dataframe(pd.DataFrame(top_cases))
    else:
        st.caption("Sin casos destacados.")

    with st.expander("Ver respuesta completa"):
        st.json(resp)
