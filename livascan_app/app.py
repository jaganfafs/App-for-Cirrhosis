import streamlit as st

st.set_page_config(
    page_title="LivaScan AI",
    page_icon="🩺",
    layout="wide"
)

# Load global CSS
with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# Redirect to Home page
st.switch_page("pages/Home.py")

