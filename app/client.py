import streamlit as st

from components.sidebar import render_sidebar, SidebarConfig
from components.uploader import render_uploader
from components.results import render_results
from config.api_config import call_analyze


def main():
    st.set_page_config(page_title="MeLi RBA Anomaly Dashboard", layout="wide")

    st.title("RBA Anomaly — Dashboard (Client)")

    st.write("Config actual:")
    cfg: SidebarConfig = render_sidebar()
    st.code(repr(cfg), language="python")
    payload, total = render_uploader(limit=cfg.limit)
    run = st.button("Analizar", type="primary", disabled=not payload)

    if run:
        with st.spinner("Llamando a la API..."):
            try:
                resp = call_analyze(cfg.base_url, payload)
                render_results(resp)
            except Exception as e:
                st.error(f"Error al llamar la API: {e}")


if __name__ == "__main__":
    main()
