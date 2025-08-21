import streamlit as st

from components.sidebar import render_sidebar, SidebarConfig


def main():
    st.set_page_config(page_title="MeLi RBA Anomaly Dashboard", layout="wide")
    cfg: SidebarConfig = render_sidebar()

    st.title("RBA Anomaly — Dashboard (Client)")
    st.write("Config actual:")
    st.code(repr(cfg), language="python")


if __name__ == "__main__":
    main()
