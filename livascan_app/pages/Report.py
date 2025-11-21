import streamlit as st
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Report", page_icon="📄", layout="wide")

css_path = "livascan_app/style.css"
if os.path.exists(css_path):
    with open(css_path) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

report_img = "livascan_app/assets/report.png"
if os.path.exists(report_img):
    st.image(report_img, use_column_width=True)

st.markdown("<h2 class='section-title'>Patient Report</h2>", unsafe_allow_html=True)

result = st.session_state.get("ai_result", None)
if result is None:
    st.error("No AI result available. Please run the scan first.")
    if st.button("Go to Scan"):
        st.switch_page("pages/Scan.py")
    st.stop()

labels = ["Healthy", "Borderline", "Cirrhosis"]
label = labels[result] if result in [0,1,2] else "Unknown"

st.markdown(f"### Final Classification: **{label}**")

# simple visual
fig, ax = plt.subplots(figsize=(4,4))
ax.pie([1], labels=[label], autopct="%1.1f%%", startangle=90)
ax.axis('equal')
st.pyplot(fig)

st.download_button("Download basic report (txt)", data=f"Result: {label}\n", file_name="livascan_report.txt")

