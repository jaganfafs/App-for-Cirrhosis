import streamlit as st
import os

st.set_page_config(page_title="Insights", page_icon="📊", layout="wide")

css_path = "livascan_app/style.css"
if os.path.exists(css_path):
    with open(css_path) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

ins_img = "livascan_app/assets/insights.png"
if os.path.exists(ins_img):
    st.image(ins_img, use_column_width=True)

st.markdown("<h2 class='section-title'>Clinical Insights</h2>", unsafe_allow_html=True)

result = st.session_state.get("ai_result", None)
if result is None:
    st.warning("No AI result found. Run the AI Scan first.")
    if st.button("Go to Scan"):
        st.switch_page("pages/Scan.py")
    st.stop()

labels = ["Healthy Liver", "Borderline Condition", "Cirrhosis Suspected"]
category = labels[result] if result in [0,1,2] else "Unknown"

st.markdown(f"### 🚑 Condition Detected: **{category}**")

st.markdown("""
#### 🩺 Medical Interpretation - Seven key points
1. MRI texture and intensity features indicate the detected condition.
2. Analysis uses paired T1/T2 features to assess fibrosis-related changes.
3. A healthy liver shows uniform parenchymal signal and no nodularity.
4. Borderline cases demonstrate subtle signal irregularities—recommend follow-up tests.
5. Cirrhosis-suspected shows architectural distortion and nodular patterns on imaging.
6. AI findings are probabilistic — correlate with labs (LFTs), elastography, and clinical exam.
7. Follow-up by hepatology is recommended for management and possible biopsy if indicated.
""")

if st.button("View Patient Report"):
    st.switch_page("pages/Report.py")

