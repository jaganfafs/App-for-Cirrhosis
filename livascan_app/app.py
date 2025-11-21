import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="LivaScan AI",
    page_icon="🩺",
    layout="wide"
)

# Load CSS
with open("livascan_app/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# HERO SECTION
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<h1 class='title'>LivaScan AI – Advanced Cirrhosis Detection</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p class='description'>
    A next-generation AI companion that analyzes paired liver MRI scans to support early detection of cirrhosis 
    and guide clinical decision-making.
    </p>
    """, unsafe_allow_html=True)

    if st.button("GET STARTED", use_container_width=False):
        st.switch_page("pages/Services.py")

with col2:
    hero = Image.open("assets/hero.png")
    st.image(hero, use_column_width=True)

