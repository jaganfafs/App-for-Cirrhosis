import streamlit as st

st.set_page_config(page_title="Insights", page_icon="📊", layout="wide")

with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.image("livascan_app/assets/insights.png", use_column_width=True) 

st.markdown("<h2 class='section-title'>Clinical Insights</h2>", unsafe_allow_html=True)

result = st.session_state.get("ai_result", None)

if result is None:
    st.warning("Please run the AI scan first.")
    st.stop()

labels = ["Healthy Liver", "Borderline Condition", "Cirrhosis Suspected"]
category = labels[result]

st.markdown(f"### 🚑 Condition Detected: **{category}**")

st.markdown("""
#### 🩺 Clinical Interpretation

1. MRI liver segmentation reveals tissue characteristics consistent with the detected condition.
2. T1 and T2 intensity variations have been analyzed for fibrosis patterns.
3. No major architectural distortion is seen in healthy cases.
4. Borderline cases show mild irregularities requiring clinical correlation.
5. Cirrhosis-suspected cases show nodular margins and regenerative pattern changes.
6. AI analysis helps assist radiologists—not replace clinical judgment.
7. Please consult a hepatologist for appropriate medical evaluation.
""")

if st.button("View Report"):
    st.switch_page("pages/Report.py")


