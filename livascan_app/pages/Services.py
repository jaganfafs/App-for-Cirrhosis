import streamlit as st
from PIL import Image

st.set_page_config(page_title="Our Services", page_icon="🧪", layout="wide")

with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.markdown("<h1 class='section-title'>Our Services</h1>", unsafe_allow_html=True)

st.image("assets/services.png", use_column_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("AI Liver Scan"):
        st.switch_page("pages/Scan.py")

with col2:
    if st.button("Clinical Insights"):
        st.switch_page("pages/Insights.py")

with col3:
    if st.button("Patient Report"):
        st.switch_page("pages/Report.py")
