from graph.pipeline_state import PipelineState


def build_report(state: PipelineState) -> PipelineState:
    if "df_raw" not in state or "predictions" not in state or "scores" not in state:
        raise ValueError("report: faltan df_raw / predictions / scores; ejecuta ingest, transform y predict primero")

    df = state["df_raw"].copy()
    preds = state["predictions"]
    scores = state["scores"]

    df["anomaly"] = preds
    df["score"] = scores

    total = int(len(df))
    anomalies = int(df["anomaly"].sum()) if total else 0
    anomaly_rate = float(anomalies / total) if total else 0.0

    login_success_rate = float(df["login_successful"].mean()) if "login_successful" in df.columns and total else None

    by_country = None
    if "country" in df.columns:
        tmp = df.groupby("country")["anomaly"].agg(count="count", anomalies="sum")
        tmp["anomaly_rate"] = tmp["anomalies"] / tmp["count"]
        by_country = tmp.reset_index().sort_values("anomaly_rate", ascending=False).head(10).to_dict(orient="records")

    by_device = None
    if "device_type" in df.columns:
        tmp = df.groupby("device_type")["anomaly"].agg(count="count", anomalies="sum")
        tmp["anomaly_rate"] = tmp["anomalies"] / tmp["count"]
        by_device = tmp.reset_index().sort_values("anomaly_rate", ascending=False).to_dict(orient="records")

    top_cases_cols = [c for c in
                      ["ip_address", "country", "device_type", "os_name_and_version", "browser_name_and_version",
                       "anomaly", "score"] if c in df.columns]
    top_cases = df.sort_values("score", ascending=True).head(5)[top_cases_cols].to_dict(orient="records")

    state["report_df"] = df
    state["report_summary"] = {
        "total": total,
        "anomalies": anomalies,
        "anomaly_rate": round(anomaly_rate, 4),
        "login_success_rate": round(login_success_rate, 4) if login_success_rate is not None else None,
        "by_country": by_country,
        "by_device": by_device,
        "top_cases": top_cases,
    }
    return state
