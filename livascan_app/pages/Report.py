# livascan_app/pages/Report.py
import streamlit as st
import matplotlib.pyplot as plt
import os
from livascan_app import utils

st.set_page_config(layout="wide")
ROOT = utils.project_root()

st.title("AI Report")

res = st.session_state.get("analysis_result", None)
if res is None:
    st.info("No analysis result found. Please run analysis in the Scan page first.")
    st.stop()

mean_prob = res["mean_prob"]
slices_total = res["slices_total"]
slices_cirr = res["slices_cirr"]
slices_healthy = res["slices_healthy"]

# Decide label based on your thresholds
LOWER = 0.455
UPPER = 0.475
if mean_prob < LOWER:
    label = "Healthy"
    color_box = "#d4f7e2"
    header = "Healthy (AI)"
elif mean_prob > UPPER:
    label = "Cirrhosis"
    color_box = "#ffe7e6"
    header = "⚠️ Cirrhosis (AI)"
else:
    label = "Borderline / Inconclusive"
    color_box = "#fff3cd"
    header = "Borderline / Inconclusive (AI)"

st.markdown(f"<div style='background:{color_box};padding:20px;border-radius:10px;'><h2>{header}</h2>"
            f"<p>Mean estimated cirrhosis probability: <b>{mean_prob*100:.2f}%</b></p></div>",
            unsafe_allow_html=True)

st.write(f"Total slices analysed: **{slices_total}**")
st.write(f"Slices cirrhosis-leaning: **{slices_cirr}**")
st.write(f"Slices healthy-leaning: **{slices_healthy}**")

# Bar chart: slices counts
fig, ax = plt.subplots(figsize=(5,3))
ax.bar(["Cirrhosis", "Healthy"], [slices_cirr, slices_healthy], color=["#ff6b6b","#7ec8ff"])
ax.set_ylabel("Slice count")
ax.set_ylim(0, max(1,slices_total))
for i,v in enumerate([slices_cirr, slices_healthy]):
    ax.text(i, v + 0.05*max(1,slices_total), str(v), ha='center')
st.pyplot(fig)

# Clinical 7-point description (medical text)
st.subheader("Clinical interpretation — plain English (for clinicians/patient summary)")
if label == "Cirrhosis":
    points = [
        "1. The AI estimates an elevated probability of cirrhosis on this study.",
        "2. Imaging appearances suggest chronic parenchymal remodeling and fibrosis.",
        "3. Correlate with clinical history (alcohol, viral hepatitis, metabolic syndrome).",
        "4. Recommend correlation with liver function tests (LFTs) and elastography if available.",
        "5. Consider referral to hepatology for assessment and staging (if not already followed).",
        "6. If clinically indicated, biopsy may be considered for definitive staging/etiology.",
        "7. Management should include risk-factor modification, monitoring, and appropriate surveillance for complications (varices, HCC) per guideline."
    ]
elif label == "Borderline / Inconclusive":
    points = [
        "1. The AI result lies in a borderline range and is not definitive.",
        "2. Imaging features are equivocal; subtle changes may be present.",
        "3. Correlate with clinical data and laboratory tests (LFTs, fibrosis markers).",
        "4. Consider further quantitative testing (elastography) or short-term imaging follow-up.",
        "5. If risk factors present, discuss hepatology referral for evaluation.",
        "6. Avoid over-interpretation; combine imaging with clinical context before decisions.",
        "7. Repeat imaging or additional tests may clarify the diagnosis."
    ]
else:  # Healthy
    points = [
        "1. The AI estimates a relatively low probability of cirrhosis on this study.",
        "2. Imaging features appear more consistent with preserved hepatic architecture.",
        "3. Correlate with clinical history and liver function tests to confirm.",
        "4. If clinical suspicion remains, consider elastography for additional reassurance.",
        "5. Counsel on prevention and risk factor modification when applicable.",
        "6. Routine surveillance as per clinical context — no specific cirrhosis surveillance indicated.",
        "7. If new symptoms or abnormal labs appear, re-evaluate with clinical team."
    ]

for p in points:
    st.markdown(f"<p style='margin:6px 0'>{p}</p>", unsafe_allow_html=True)

st.markdown("---")
st.button("Analyze another study", on_click=lambda: st.session_state.clear())

