from dataclasses import dataclass
import streamlit as st


@dataclass
class SidebarConfig:
    limit: int


def render_sidebar() -> SidebarConfig:
    st.sidebar.title("RBA Anomaly — Panel de control")

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

    return SidebarConfig(limit=limit)
