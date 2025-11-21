# livascan_app/pages/Home.py
import streamlit as st
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"

st.set_page_config(page_title="Home - LivaScan", page_icon="🏥", layout="wide")

css_path = BASE_DIR / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])
with col1:
    st.markdown("<h1 class='title'>LivaScan AI — Advanced Cirrhosis Detection</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='description'>Upload paired T1 and T2 MRI scans and let the AI provide a clinicalsummary, insights and a downloadable report.</p>",
        unsafe_allow_html=True,
    )
    if st.button("Get Started"):
        # Navigate to Scan page — Streamlit pages are shown in the left menu
        st.experimental_set_query_params(page="Scan")
with col2:
    hero = ASSETS / "hero.png"
    if hero.exists():
        st.image(Image.open(hero), use_column_width=True)
    else:
        st.info("Put hero.png in livascan_app/assets to show the hero image.")

