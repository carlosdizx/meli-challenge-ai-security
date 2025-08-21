import streamlit as st

from components.sidebar import render_sidebar, SidebarConfig
from components.uploader import render_uploader


def main():
    st.set_page_config(page_title="MeLi RBA Anomaly Dashboard", layout="wide")

    st.title("RBA Anomaly — Dashboard (Client)")

    st.write("Config actual:")
    cfg: SidebarConfig = render_sidebar()
    st.code(repr(cfg), language="python")
    render_uploader(cfg.limit)


if __name__ == "__main__":
    main()
