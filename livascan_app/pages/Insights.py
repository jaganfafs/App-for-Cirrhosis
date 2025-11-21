# livascan_app/pages/Insights.py
import streamlit as st
from livascan_app import utils
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
css_path = BASE_DIR / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Clinical Insights")

res = st.session_state.get("last_result", None)
if res is None:
    st.info("No analysis results available yet. Please run analysis in the Scan page.")
else:
    mean_prob = res["mean_prob"]
    st.subheader("Summary")
    st.markdown(f"- Mean estimated cirrhosis probability: **{mean_prob*100:.2f}%**")
    st.markdown(f"- Slices cirrhosis-leaning: **{res['slices_cirr']}**")
    st.markdown(f"- Slices healthy-leaning: **{res['slices_healthy']}**")

    # Visual: donut percent
    fig, ax = plt.subplots(figsize=(3,3))
    sizes = [mean_prob, 1-mean_prob]
    colors = ["#f97373", "#2b9af3"]
    ax.pie(sizes, wedgeprops=dict(width=0.5), startangle=90, colors=colors)
    ax.set(aspect="equal")
    ax.text(0, 0, f"{mean_prob*100:.1f}%", ha="center", va="center", fontsize=14)
    st.pyplot(fig)

    # Detailed textual clinical insights (6-7 bullets)
    st.markdown("### Clinical interpretation (short)")
    # NOTE: these are templated suggestions for clinician review — not definitive diagnosis.
    st.markdown(
        """
- 1. The AI estimates a **higher** probability of cirrhosis when mean probability > 0.47 — correlate clinically.
- 2. Consider liver function tests (LFTs) and elastography for quantitative fibrosis assessment.
- 3. If symptoms (jaundice, ascites, variceal bleeding) are present — urgent specialist review is recommended.
- 4. Imaging patterns suggestive of cirrhosis include nodular surface, volume redistribution and regenerative nodules.
- 5. Consider additional contrast-enhanced MRI or biopsy if imaging and labs are discordant.
- 6. If the AI result is borderline, schedule follow-up imaging in 3–6 months or multimodal assessment.
- 7. Always correlate with clinical history, alcohol / viral hepatitis risk factors, and biochemical tests.
"""
    )

    # show small bar chart of slice counts
    counts = {"Cirrhosis": res["slices_cirr"], "Healthy": res["slices_healthy"]}
    fig2 = utils.bar_plot_counts(counts, labels=("Cirrhosis","Healthy"))
    st.pyplot(fig2)

