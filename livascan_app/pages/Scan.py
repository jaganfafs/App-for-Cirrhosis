import streamlit as st
import os
import nibabel as nib
import numpy as np
import joblib
import tempfile
import time

st.set_page_config(page_title="AI Scan", page_icon="🧬", layout="wide")

# ----------------------
# CSS (repo-root relative)
# ----------------------
css_path = "livascan_app/style.css"
if os.path.exists(css_path):
    with open(css_path) as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# ----------------------
# Header + illustration
# ----------------------
st.markdown("<h1 class='page-title'>Upload T1 & T2 MRI Scans</h1>", unsafe_allow_html=True)
st.markdown("Upload paired T1 and T2 NIfTI volumes (.nii or .nii.gz). Keep PHI out of public demos.", unsafe_allow_html=True)

# ----------------------
# Upload widgets
# ----------------------
t1 = st.file_uploader("Upload T1 MRI (.nii / .nii.gz)", type=["nii", "nii.gz"], key="t1_upload")
t2 = st.file_uploader("Upload T2 MRI (.nii / .nii.gz)", type=["nii", "nii.gz"], key="t2_upload")

# ----------------------
# Helper: save UploadedFile to temp file and return path
# ----------------------
def save_uploaded_to_temp(uploaded_file):
    if uploaded_file is None:
        return None
    # determine suffix from filename
    name = uploaded_file.name
    _, ext = os.path.splitext(name)
    # if .nii.gz, ext will be .gz so handle
    if name.lower().endswith(".nii.gz"):
        suffix = ".nii.gz"
    else:
        suffix = ext if ext else ""
    tf = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    try:
        # uploaded_file.read() returns bytes
        tf.write(uploaded_file.read())
        tf.flush()
        tf.close()
        return tf.name
    except Exception as e:
        tf.close()
        if os.path.exists(tf.name):
            os.remove(tf.name)
        raise e

# ----------------------
# Model path
# ----------------------
model_path = "livascan_app/model/RandomForest_Cirrhosis.pkl"

# ----------------------
# Run analysis
# ----------------------
if st.button("Start AI Analysis"):

    # basic checks
    if t1 is None or t2 is None:
        st.error("Please upload both T1 and T2 NIfTI files before starting analysis.")
    else:
        # Save uploaded files to disk
        try:
            with st.spinner("Saving uploaded files..."):
                t1_path = save_uploaded_to_temp(t1)
                t2_path = save_uploaded_to_temp(t2)
        except Exception as e:
            st.error(f"Failed to save uploaded files: {e}")
            st.stop()

        # Load volumes safely
        try:
            with st.spinner("Loading NIfTI volumes..."):
                # nib.load expects a filename (string) or fileobj; we use filename
                vol_t1 = nib.load(t1_path).get_fdata().astype(np.float32)
                vol_t2 = nib.load(t2_path).get_fdata().astype(np.float32)
        except Exception as e:
            st.error(f"Error loading NIfTI: {e}")
            # cleanup temp files
            if os.path.exists(t1_path): os.remove(t1_path)
            if os.path.exists(t2_path): os.remove(t2_path)
            st.stop()

        # basic preprocessing placeholder (demo)
        progress = st.progress(0)
        time.sleep(0.2)
        progress.progress(10)

        # For demo purposes: compute simple features (replace with ViT features in production)
        try:
            # compute simple slice-wise mean intensities
            feat_t1 = vol_t1.mean()
            feat_t2 = vol_t2.mean()
            features = np.array([feat_t1, feat_t2]).reshape(1, -1)
        except Exception as e:
            st.error(f"Feature extraction failed: {e}")
            if os.path.exists(t1_path): os.remove(t1_path)
            if os.path.exists(t2_path): os.remove(t2_path)
            st.stop()

        progress.progress(50)
        time.sleep(0.3)

        # Load classifier if available
        if os.path.exists(model_path):
            try:
                rf = joblib.load(model_path)
                prob = None
                # If classifier supports predict_proba:
                if hasattr(rf, "predict_proba"):
                    probs = rf.predict_proba(features)[:, 1]
                    # Convert to a simple label: 0 healthy, 1 borderline, 2 cirrhosis
                    # (This mapping depends on your training; adjust accordingly)
                    mean_p = float(probs.mean())
                    if mean_p < 0.455:
                        label = 0
                    elif mean_p > 0.475:
                        label = 2
                    else:
                        label = 1
                    st.session_state["ai_prob"] = mean_p
                    st.session_state["ai_slices"] = int((probs >= 0.465).sum())  # demo
                    st.session_state["ai_result"] = label
                else:
                    # fallback to predict
                    pred = rf.predict(features)[0]
                    st.session_state["ai_result"] = int(pred)
            except Exception as e:
                st.warning(f"Error loading/predicting with RandomForest: {e}")
                st.info("Using demo fallback result.")
                st.session_state["ai_result"] = 1  # borderline demo
        else:
            st.warning(f"RandomForest not found at {model_path}. Using demo fallback result.")
            st.session_state["ai_result"] = 1  # borderline demo
            st.session_state["ai_prob"] = 0.4881
            st.session_state["ai_slices"] = 21

        # finalize progress
        progress.progress(100)
        time.sleep(0.2)
        st.success("Analysis complete. Redirecting to Insights...")
        # cleanup temp files
        try:
            if os.path.exists(t1_path): os.remove(t1_path)
            if os.path.exists(t2_path): os.remove(t2_path)
        except:
            pass

        # navigate to Insights page
        st.experimental_rerun()

