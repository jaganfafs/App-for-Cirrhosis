import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Patient Report", page_icon="📄", layout="wide")

with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.image("assets/report.png", use_column_width=True)

st.markdown("<h2 class='section-title'>Patient Report</h2>", unsafe_allow_html=True)

result = st.session_state.get("ai_result", None)

if result is None:
    st.error("Please perform AI Scan first.")
    st.stop()

labels = ["Healthy", "Borderline", "Cirrhosis"]

st.markdown(f"### Final Classification: **{labels[result]}**")

# Simple pie chart
fig, ax = plt.subplots(figsize=(4, 4))
ax.pie([1], labels=[labels[result]], autopct='%1.1f%%')
st.pyplot(fig)

st.info("PDF report feature will be added soon.")

