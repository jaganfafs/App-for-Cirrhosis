# livascan_app/pages/Scan.py
import streamlit as st
from pathlib import Path
import nibabel as nib
import numpy as np
from PIL import Image
import time

from livascan_app import utils

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"

st.set_page_config(page_title="Scan - LivaScan", layout="wide")
# Load CSS
css_path = BASE_DIR / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Upload T1 & T2 MRI Scans")

t1 = st.file_uploader("Upload T1 MRI (.nii / .nii.gz)", type=["nii", "nii.gz"])
t2 = st.file_uploader("Upload T2 MRI (.nii / .nii.gz)", type=["nii", "nii.gz"])

use_demo = st.button("Use Synthetic Demo (UI demo)")
start = st.button("Start AI Analysis")

if use_demo:
    # create synthetic saved files so rest of pipeline can consume a path
    import tempfile, os
    tmp_dir = tempfile.mkdtemp()
    # generate simple synthetic numpy volumes and save as .nii
    vol = np.random.rand(64, 64, 10).astype(np.float32)
    import nibabel as nib
    nib.Nifti1Image(vol, affine=np.eye(4)).to_filename(os.path.join(tmp_dir, "demo1.nii"))
    nib.Nifti1Image(vol, affine=np.eye(4)).to_filename(os.path.join(tmp_dir, "demo2.nii"))
    t1_path = os.path.join(tmp_dir, "demo1.nii")
    t2_path = os.path.join(tmp_dir, "demo2.nii")
    st.success("Demo data ready. Click Start AI Analysis to run the demo.")
    # store in session_state
    st.session_state["demo_t1"] = t1_path
    st.session_state["demo_t2"] = t2_path

if start:
    # ensure T1/T2 saved
    try:
        if "demo_t1" in st.session_state and "demo_t2" in st.session_state:
            t1_path = st.session_state["demo_t1"]
            t2_path = st.session_state["demo_t2"]
        else:
            if t1 is None or t2 is None:
                st.error("Please upload both T1 and T2 volumes (or use Demo).")
                st.stop()
            t1_path = utils.save_uploadedfile(t1)
            t2_path = utils.save_uploadedfile(t2)

        st.info("Loading volumes...")
        # Load NIfTI safely
        try:
            vol1 = nib.load(t1_path).get_fdata().astype(np.float32)
            vol2 = nib.load(t2_path).get_fdata().astype(np.float32)
        except Exception as e:
            st.error(f"Error loading NIfTI: {e}")
            st.stop()

        n_slices = min(vol1.shape[2], vol2.shape[2])
        st.write(f"Detected {n_slices} slices. Running lightweight feature extraction...")

        # Very small demo of per-slice features: mean + std (2 features) -> NOT real ViT
        feats = []
        for i in range(n_slices):
            s1 = vol1[:, :, i]
            s2 = vol2[:, :, i]
            f = [np.nanmean(s1), np.nanstd(s1), np.nanmean(s2), np.nanstd(s2)]
            feats.append(f)
        X = np.array(feats)  # shape (n_slices, 4)

        st.progress(0.2)
        # Attempt to load RandomForest
        rf_model, rf_err = utils.load_rf_model()
        probs = None
        if rf_model is None:
            st.warning(f"RandomForest not loaded: {rf_err}. Using demo fallback.")
            probs = utils.demo_result(n_slices)
        else:
            # Try predict_proba
            try:
                if X.shape[1] != rf_model.n_features_in_:
                    st.warning(f"Model expects {rf_model.n_features_in_} features but we have {X.shape[1]}. Using demo fallback.")
                    probs = utils.demo_result(n_slices)
                else:
                    proba = rf_model.predict_proba(X)[:, 1]
                    probs = proba
            except Exception as e:
                st.error(f"Error loading/predicting with RandomForest: {e}")
                st.info("Using demo fallback instead.")
                probs = utils.demo_result(n_slices)

        st.progress(0.8)
        # compute summary
        mean_prob = float(np.mean(probs))
        slice_mask = probs >= 0.465
        slices_cirr = int(slice_mask.sum())
        slices_healthy = int(len(probs) - slices_cirr)

        # store results to session_state for Insights/Report pages
        st.session_state["last_result"] = {
            "mean_prob": mean_prob,
            "probs": probs.tolist(),
            "slices_cirr": slices_cirr,
            "slices_healthy": slices_healthy,
            "n_slices": n_slices,
        }
        st.success("Analysis complete. Redirecting to Insights...")
        time.sleep(0.8)
        # go to Insights page (Streamlit Pages should be selected manually from left menu)
        st.experimental_set_query_params(page="Insights")
        st.experimental_rerun()

    except Exception as e:
        st.exception(e)

