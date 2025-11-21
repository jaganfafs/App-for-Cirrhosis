# livascan_app/pages/Services.py
import streamlit as st
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"

css_path = BASE_DIR / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Our Services")
st.write("Click a service to jump to the relevant page (Scan / Insights / Report).")

col1, col2, col3 = st.columns(3)
with col1:
    st.image(Image.open(ASSETS / "scan.png") if (ASSETS / "scan.png").exists() else None)
    if st.button("AI Liver Scan"):
        st.experimental_set_query_params(page="Scan")

with col2:
    st.image(Image.open(ASSETS / "insights.png") if (ASSETS / "insights.png").exists() else None)
    if st.button("Clinical Insights"):
        st.experimental_set_query_params(page="Insights")

with col3:
    st.image(Image.open(ASSETS / "report.png") if (ASSETS / "report.png").exists() else None)
    if st.button("Patient Report"):
        st.experimental_set_query_params(page="Report")

