import streamlit as st
import os

st.set_page_config(page_title="Services", page_icon="🧪", layout="wide")

# CSS path (repo-root relative)
css_path = "livascan_app/style.css"
if os.path.exists(css_path):
    with open(css_path) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
else:
    st.error(f"❌ style.css not found at: {css_path}")

st.markdown("<h1 class='section-title'>Our Services</h1>", unsafe_allow_html=True)

# image
services_path = "livascan_app/assets/services.png"
if os.path.exists(services_path):
    st.image(services_path, use_column_width=True)
else:
    st.warning(f"services image missing at: {services_path}")

st.write("")  # spacing

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("AI Liver Scan"):
        st.experimental_set_query_params(page="scan")
        st.switch_page("pages/Scan.py")
with col2:
    if st.button("Clinical Insights"):
        st.switch_page("pages/Insights.py")
with col3:
    if st.button("Patient Report"):
        st.switch_page("pages/Report.py")

