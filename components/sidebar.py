from dataclasses import dataclass
import streamlit as st


@dataclass
class SidebarConfig:
    base_url: str
    limit: int


def render_sidebar(default_base_url: str = "http://localhost:4200") -> SidebarConfig:
    st.sidebar.title("RBA Anomaly — Panel de control")

    base_url = st.sidebar.text_input("API base URL", value=default_base_url).rstrip("/")
    limit = st.sidebar.slider("Máx. registros a enviar", min_value=1, max_value=2000, value=200, step=50)

    st.sidebar.divider()
    st.sidebar.title("Acerca de mi")
    st.sidebar.markdown("""
    <div style="display: flex; justify-content: space-between; width: 100%;">
        <a href="https://www.linkedin.com/in/carlos-ernesto-diaz-basante/" target="_blank">
            <img src="https://img.icons8.com/color/48/000000/linkedin.png" width="32">
        </a>
        <a href="https://github.com/carlosdizx" target="_blank">
            <img src="https://img.icons8.com/ios-filled/50/000000/github.png" width="32">
        </a>
        <a href="https://ernesto-diaz.streamlit.app/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/9144/9144593.png" width="32">
        </a>
    </div>
    """, unsafe_allow_html=True)

    return SidebarConfig(base_url=base_url, limit=limit)
