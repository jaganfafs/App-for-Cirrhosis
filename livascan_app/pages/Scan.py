# livascan_app/pages/Scan.py
import streamlit as st
import os
import time
import joblib
import numpy as np
import matplotlib.pyplot as plt

from livascan_app import utils

st.set_page_config(layout="wide")
ROOT = utils.project_root()

# Paths
MODEL_PATH = os.path.join(ROOT, "model", "RandomForest_Cirrhosis.pkl")

# Helper: simple progress simulation for UI
def simulated_progress(progress_bar, start=0.0, end=1.0, duration=1.5):
    steps = 30
    for i in range(steps+1):
        frac = start + (end-start) * (i/steps)
        progress_bar.progress(min(frac,1.0))
        time.sleep(duration/steps)

# Load RF (if present)
rf_model = None
rf_missing = False
if os.path.exists(MODEL_PATH):
    try:
        rf_model = joblib.load(MODEL_PATH)
    except Exception as e:
        st.warning(f"Warning: could not load RandomForest model: {e}")
        rf_model = None
else:
    rf_missing = True

st.title("Upload T1 & T2 MRI Scans")

c1, c2 = st.columns([1, 2])
with c1:
    t1_file = st.file_uploader("Upload T1 MRI (.nii / .nii.gz)", type=["nii", "nii.gz"], key="t1")
    t2_file = st.file_uploader("Upload T2 MRI (.nii / .nii.gz)", type=["nii", "nii.gz"], key="t2")

with c2:
    st.info("Tip: use scans from the same patient and matching T1/T2 series.")
    status_placeholder = st.empty()
    progress_bar = st.progress(0.0)

if st.button("Start AI Analysis"):
    # Basic validation
    if t1_file is None or t2_file is None:
        st.error("Please upload both T1 and T2 files.")
        st.stop()

    try:
        status_placeholder.info("Saving uploaded files...")
        t1_path = utils.save_uploaded_file(t1_file)
        t2_path = utils.save_uploaded_file(t2_file)

        status_placeholder.info("Loading NIfTI volumes...")
        import nibabel as nib
        t1_vol = nib.load(t1_path).get_fdata().astype(np.float32)
        t2_vol = nib.load(t2_path).get_fdata().astype(np.float32)

        status_placeholder.info("Preprocessing slices...")
        # --- Insert your preprocess_slice and vit extraction pipeline here ---
        # For demonstration: we will create *fake* features shaped to match rf_model if available.
        # If you already have functions vit_extract_batch / preprocess_slice, call them instead.

        simulated_progress(progress_bar, start=0.0, end=0.35, duration=0.6)

        # Example: create slice features (this should be replaced by your real ViT pipeline)
        # Suppose each slice becomes a 768-dim feature and fused -> 1536 dims (model trained on that)
        # We'll attempt to extract N slices and produce a fused array shaped (n_slices, feat_dim)
        # --- REPLACE this block with your real feature extraction ---
        n_slices = min(t1_vol.shape[2], t2_vol.shape[2])
        if n_slices <= 0:
            raise ValueError("No slices in volumes.")
        # placeholder: fake features (this must become your vit features)
        fake_feat_dim_each = 768
        t1_feats = np.random.rand(n_slices, fake_feat_dim_each).astype(np.float32)
        t2_feats = np.random.rand(n_slices, fake_feat_dim_each).astype(np.float32)
        fused = np.concatenate([t1_feats, t2_feats], axis=1)  # shape (n_slices, 1536)

        simulated_progress(progress_bar, start=0.35, end=0.65, duration=0.6)

        # Run classifier safely
        if rf_model is None:
            st.warning("RandomForest model not available — using demo fallback result.")
            probs = np.linspace(0.3, 0.7, fused.shape[0])  # demo
        else:
            # check expected feature size
            expected = getattr(rf_model, "n_features_in_", None)
            if expected is None:
                # older pickles may not have n_features_in_ -> try to predict and catch
                try:
                    probs = rf_model.predict_proba(fused)[:,1]
                except Exception as e:
                    st.error(f"Error predicting with RandomForest: {e}")
                    st.warning("Using demo fallback result.")
                    probs = np.linspace(0.3, 0.7, fused.shape[0])
            else:
                if fused.shape[1] != expected:
                    st.warning(
                        f"Error loading/predicting with RandomForest: X has {fused.shape[1]} features, "
                        f"but RandomForestClassifier expected {expected} features as input."
                    )
                    st.info("Using demo fallback result.")
                    probs = np.linspace(0.3, 0.7, fused.shape[0])
                else:
                    probs = rf_model.predict_proba(fused)[:,1]

        mean_prob = float(probs.mean())
        slices_total = len(probs)
        slices_cirr = int((probs >= 0.465).sum())  # your threshold
        slices_healthy = slices_total - slices_cirr

        simulated_progress(progress_bar, start=0.65, end=1.0, duration=0.7)
        status_placeholder.success("Analysis complete. Redirecting to Insights...")

        # Save results to session state so Report/Insights pages can read them
        st.session_state["analysis_result"] = dict(
            mean_prob = mean_prob,
            slices_total = slices_total,
            slices_cirr = slices_cirr,
            slices_healthy = slices_healthy,
            probs = probs.tolist()
        )

        # redirect to Insights (or Report)
        st.experimental_rerun()

    except Exception as e:
        st.error(f"Error during processing: {e}")
        raise

