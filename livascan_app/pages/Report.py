# livascan_app/pages/Report.py
import streamlit as st
from pathlib import Path
from matplotlib import pyplot as plt
import io
from livascan_app import utils

BASE_DIR = Path(__file__).resolve().parent.parent
css_path = BASE_DIR / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Patient Report")

res = st.session_state.get("last_result", None)
if res is None:
    st.info("No report available. Run Scan first.")
else:
    mean_prob = res["mean_prob"]
    # Big alert box
    if mean_prob > 0.475:
        st.warning("⚠️ Cirrhosis (AI): Elevated model-estimated probability. Correlate clinically.")
    elif mean_prob < 0.455:
        st.success("✅ Healthy (AI): Probability below threshold.")
    else:
        st.info("ℹ️ Borderline / Inconclusive (AI). Seek expert review.")

    st.markdown(f"**Mean estimated cirrhosis probability:** {mean_prob*100:.2f}%")
    st.markdown(f"- Slices cirrhosis-leaning: **{res['slices_cirr']}**")
    st.markdown(f"- Slices healthy-leaning: **{res['slices_healthy']}**")

    # show bar plot using utils
    counts = {"Cirrhosis": res["slices_cirr"], "Healthy": res["slices_healthy"]}
    fig = utils.bar_plot_counts(counts, labels=("Cirrhosis","Healthy"))
    st.pyplot(fig)

    # Provide a downloadable simple MD report
    md = [
        "# LivaScan AI Report",
        f"- Mean probability: {mean_prob*100:.2f}%",
        f"- Slices cirrhosis-leaning: {res['slices_cirr']}",
        f"- Slices healthy-leaning: {res['slices_healthy']}",
        "",
        "### Clinical notes",
        "- Automated result — clinician interpretation required."
    ]
    md_bytes = "\n".join(md).encode("utf-8")
    st.download_button("Download report (MD)", data=md_bytes, file_name="LivaScan_report.md")

