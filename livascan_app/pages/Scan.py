import streamlit as st
import nibabel as nib
import numpy as np
import joblib

st.set_page_config(page_title="AI Scan", page_icon="🧬", layout="wide")

# Load CSS
with open("style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

st.image("assets/scan.png", use_column_width=True)

st.markdown("<h2 class='section-title'>Upload T1 & T2 MRI Scans</h2>", unsafe_allow_html=True)

t1_file = st.file_uploader("Upload T1 MRI (.nii/.nii.gz)", type=["nii", "nii.gz"])
t2_file = st.file_uploader("Upload T2 MRI (.nii/.nii.gz)", type=["nii", "nii.gz"])

# Load RF model
model = joblib.load("model/RandomForest_Cirrhosis.pkl")

def load_nifti(uploaded_file):
    return nib.load(uploaded_file).get_fdata()

if st.button("Start AI Analysis"):
    if not t1_file or not t2_file:
        st.error("Please upload both T1 and T2 scans.")
        st.stop()

    with st.spinner("Processing MRI scans..."):
        t1 = load_nifti(t1_file)
        t2 = load_nifti(t2_file)

        # dummy features (replace with features from your ViT later)
        features = np.array([t1.mean(), t2.mean()]).reshape(1, -1)

        result = model.predict(features)[0]
        st.session_state["ai_result"] = int(result)

    st.success("Analysis complete! Redirecting...")
    st.switch_page("pages/Insights.py")

