import streamlit as st
import os
import nibabel as nib
import numpy as np
import joblib

st.set_page_config(page_title="AI Scan", page_icon="🧬", layout="wide")

# CSS
css_path = "livascan_app/style.css"
if os.path.exists(css_path):
    with open(css_path) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
else:
    st.error(f"❌ style.css not found at: {css_path}")

# Image
scan_img = "livascan_app/assets/scan.png"
if os.path.exists(scan_img):
    st.image(scan_img, use_column_width=True)

st.markdown("<h2 class='section-title'>Upload T1 & T2 MRI Scans</h2>", unsafe_allow_html=True)

t1 = st.file_uploader("Upload T1 MRI (.nii / .nii.gz)", type=["nii", "nii.gz"])
t2 = st.file_uploader("Upload T2 MRI (.nii / .nii.gz)", type=["nii", "nii.gz"])

# Model path (only loaded when running)
model_path = "livascan_app/model/RandomForest_Cirrhosis.pkl"

def safe_load_nifti(uploaded_file):
    try:
        return nib.load(uploaded_file).get_fdata()
    except Exception as e:
        st.error(f"Error loading NIfTI: {e}")
        return None

if st.button("Start AI Analysis"):
    if t1 is None or t2 is None:
        st.error("Please upload both T1 and T2 files.")
    else:
        with st.spinner("Processing..."):
            t1_arr = safe_load_nifti(t1)
            t2_arr = safe_load_nifti(t2)
            if t1_arr is None or t2_arr is None:
                st.stop()
            # Simple placeholder features: mean intensities (replace with ViT features later)
            feats = np.array([t1_arr.mean(), t2_arr.mean()]).reshape(1, -1)

            if not os.path.exists(model_path):
                st.warning(f"RandomForest not found at {model_path}. Please upload the pickle to the repo 'model' folder.")
                # store a dummy result for UI demo (e.g., borderline)
                st.session_state["ai_result"] = 1
            else:
                try:
                    rf = joblib.load(model_path)
                    pred = rf.predict(feats)[0]
                    st.session_state["ai_result"] = int(pred)
                except Exception as e:
                    st.error(f"Error loading/predicting with RandomForest: {e}")
                    st.stop()

        st.success("Analysis finished — opening Insights...")
        st.switch_page("pages/Insights.py")

