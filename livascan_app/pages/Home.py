import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# Load CSS
with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<h1 class='title'>LivaScan AI – Advanced Cirrhosis Detection</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p class='description'>
        A next-generation AI companion that analyzes paired liver MRI scans 
        to support early detection of cirrhosis and guide clinical decision-making.
        </p>
    """, unsafe_allow_html=True)

    if st.button("GET STARTED"):
        st.switch_page("pages/Services.py")

with col2:
    st.image("livascan_app/assets/hero.png", use_column_width=True)


