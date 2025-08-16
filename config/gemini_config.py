import streamlit as st


@st.cache_resource
def get_gemini_config():
    return {
        "api_key": st.secrets["GEMINI_API_KEY"],
        "model_name": st.secrets["GEMINI_MODEL"]
    }

