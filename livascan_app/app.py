# livascan_app/app.py
import streamlit as st
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="LivaScan AI", page_icon="🩺", layout="wide")

# Load CSS (use path relative to package root)
css_path = BASE_DIR / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("style.css not found - continuing without custom styling.")

# Simple sidebar navigation (Streamlit Pages also work but keep sidebar for quick nav)
st.sidebar.title("LivaScan AI")
st.sidebar.markdown("Advanced cirrhosis detection from paired liver MRI")

# Show a simple content on the root page, link to Home page in pages/
st.title("LivaScan AI – Advanced Cirrhosis Detection")
st.write(
    "A next-generation AI companion that analyzes paired liver MRI scans to support early detection of cirrhosis."
)

col1, col2 = st.columns([1.5, 1])
with col1:
    st.markdown(
        "<h2 style='margin-bottom:0.25rem'>Welcome</h2>"
        "<p style='color:#666'>Click Get Started to go to the Home (UI) where you can begin.</p>",
        unsafe_allow_html=True,
    )
    if st.button("GET STARTED"):
        # Streamlit Pages uses the pages/ directory. If you want to route, use link text to the page
        st.markdown("Go to the **Home** item in the left sidebar (or open `/Home` page).")

with col2:
    # Show hero image if present
    hero = BASE_DIR / "assets" / "hero.png"
    if hero.exists():
        img = Image.open(hero)
        st.image(img, use_column_width=True)
    else:
        st.info("Put hero.png into livascan_app/assets to show the banner.")

st.markdown("---")
st.caption("Use the left sidebar to navigate: Home, Scan, Insights, Report, Services.")

