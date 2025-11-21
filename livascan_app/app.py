import streamlit as st
from PIL import Image
import os

# ------------------------------
# STREAMLIT PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="LivaScan AI",
    page_icon="🩺",
    layout="wide"
)

# ------------------------------
# LOAD CSS FROM CORRECT PATH
# ------------------------------
css_path = "livascan_app/style.css"
if os.path.exists(css_path):
    with open(css_path) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
else:
    st.error(f"❌ CSS file not found at: {css_path}")

# ------------------------------
# HERO SECTION
# ------------------------------

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<h1 class='title'>LivaScan AI – Advanced Cirrhosis Detection</h1>", unsafe_allow_html=True)

    st.markdown("""
    <p class='description'>
    A next-generation AI companion that analyzes paired liver MRI scans to support early detection of cirrhosis 
    and guide clinical decision-making.
    </p>
    """, unsafe_allow_html=True)

    if st.button("GET STARTED", key="start"):
        st.switch_page("pages/Services.py")

with col2:
    hero_path = "livascan_app/assets/hero.png"
    if os.path.exists(hero_path):
        hero = Image.open(hero_path)
        st.image(hero, use_column_width=True)
    else:
        st.error(f"❌ Hero image not found at: {hero_path}")

