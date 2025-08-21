from typing import List, Dict, Any
import requests
import streamlit as st


@st.cache_data(show_spinner=False)
def call_analyze(base_url: str, body: List[Dict[str, Any]]) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/analyze/"
    r = requests.post(url, json=body)
    r.raise_for_status()
    return r.json()
