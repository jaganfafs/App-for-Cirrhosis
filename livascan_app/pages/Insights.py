import streamlit as st
from PIL import Image

st.set_page_config(page_title="Clinical Insights", page_icon="📊", layout="wide")

with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.image("assets/insights.png", use_column_width=True)

st.markdown("<h2 class='section-title'>Clinical Insights</h2>", unsafe_allow_html=True)

result = st.session_state.get("ai_result", None)

if result is None:
    st.warning("No AI result found. Please upload MRI scans first.")
    st.stop()

if result == 0:
    category = "Healthy Liver"
elif result == 1:
    category = "Borderline Condition"
else:
    category = "Cirrhosis Suspected"

st.markdown(f"""
### Condition Detected: **{category}**
#### Medically Relevant Points:
- Liver tissue texture suggests {category.lower()}.
- MRI intensity patterns analyzed using paired T1 & T2 data.
- No major anatomical distortions (for healthy cases).
- Fibrosis indicators moderately present (for borderline).
- Pronounced structural irregularities (for cirrhosis).
- AI confidence based on Random Forest probability.
- Recommended to correlate clinically with liver function tests.
""")

if st.button("View Full Report"):
    st.switch_page("pages/Report.py")
