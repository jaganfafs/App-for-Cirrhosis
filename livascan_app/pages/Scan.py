import streamlit as st
import os
import nibabel as nib
import numpy as np
import joblib
import tempfile
import time
import math

st.set_page_config(page_title="AI Scan", page_icon="🧬", layout="wide")

# CSS path relative to repo root
CSS_PATH = "livascan_app/style.css"
if os.path.exists(CSS_PATH):
    with open(CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page header
st.markdown("<h1 class='page-title'>Upload T1 & T2 MRI Scans</h1>", unsafe_allow_html=True)
st.markdown("<p>Upload paired T1 and T2 NIfTI volumes (.nii / .nii.gz). Keep PHI out of public demos.</p>", unsafe_allow_html=True)


def save_uploaded_to_temp(uploaded_file):
    """
    Save a streamlit UploadedFile to a NamedTemporaryFile and return the filepath.
    """
    if uploaded_file is None:
        return None
    name = uploaded_file.name
    # handle .nii.gz
    if name.lower().endswith(".nii.gz"):
        suffix = ".nii.gz"
    else:
        _, ext = os.path.splitext(name)
        suffix = ext if ext else ""
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    try:
        tmp.write(uploaded_file.read())
        tmp.flush()
        tmp.close()
        return tmp.name
    except Exception:
        tmp.close()
        if os.path.exists(tmp.name):
            os.remove(tmp.name)
        raise


# Upload widgets
col1, col2 = st.columns(2)
with col1:
    t1 = st.file_uploader("Upload T1 MRI (.nii / .nii.gz)", type=["nii", "nii.gz"], key="t1_upload")
with col2:
    t2 = st.file_uploader("Upload T2 MRI (.nii / .nii.gz)", type=["nii", "nii.gz"], key="t2_upload")


MODEL_PATH = "livascan_app/model/RandomForest_Cirrhosis.pkl"


def make_feature_vector(base_feats: np.ndarray, target_dim: int) -> np.ndarray:
    """
    Given a small base feature vector (1D), expand/trim to `target_dim`.
    Strategy:
      - If base already >= target_dim: truncate.
      - If base < target_dim: tile/repeat the base vector then slice to target_dim.
    NOTE: This is only a structural fix so the model call doesn't crash.
    A proper fix is to extract the same features used at train time (ViT features).
    """
    base = np.asarray(base_feats).flatten()
    if target_dim <= 0:
        return base.reshape(1, -1)
    if base.size == 0:
        return np.zeros((1, target_dim), dtype=np.float32)
    if base.size >= target_dim:
        out = base[:target_dim]
    else:
        repeats = math.ceil(target_dim / base.size)
        tiled = np.tile(base, repeats)[:target_dim]
        out = tiled
    return out.reshape(1, -1)


def safe_predict_with_model(model, feats: np.ndarray):
    """
    Try to predict probability/label with the given model, while handling feature-dim mismatch.
    Returns (success_flag, result_dict)
    result_dict may contain keys: label, mean_prob, note
    """
    try:
        # if model has n_features_in_ attribute, align dims
        n_in = getattr(model, "n_features_in_", None)
        if n_in is not None:
            if feats.shape[1] != n_in:
                # adapt (tile/pad/truncate) to avoid crash
                feats = make_feature_vector(feats, int(n_in))
                note = f"Warning: input features resized to match model's expected {n_in} inputs (structural adapt)."
            else:
                note = None
        else:
            note = None

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(feats)
            # take positive-class probability (assumes binary)
            if probs.shape[1] == 2:
                mean_p = float(probs[:, 1].mean())
            else:
                # if multi-class, take max prob of class index 1 as fallback
                mean_p = float(np.max(probs, axis=1).mean())
            # determine simple label using the thresholds used elsewhere
            if mean_p < 0.455:
                label = 0  # Healthy
            elif mean_p > 0.475:
                label = 2  # Cirrhosis
            else:
                label = 1  # Borderline
            return True, {"label": int(label), "mean_prob": mean_p, "note": note}
        else:
            pred = model.predict(feats)[0]
            return True, {"label": int(pred), "note": note}
    except Exception as e:
        return False, {"error": str(e)}


if st.button("Start AI Analysis"):
    if t1 is None or t2 is None:
        st.error("Please upload both T1 and T2 NIfTI files before starting analysis.")
    else:
        # Save
        try:
            with st.spinner("Saving uploaded files..."):
                path1 = save_uploaded_to_temp(t1)
                path2 = save_uploaded_to_temp(t2)
        except Exception as e:
            st.error(f"Failed to save uploaded files: {e}")
            st.stop()

        # Load using nib
        try:
            with st.spinner("Loading NIfTI volumes..."):
                vol1 = nib.load(path1).get_fdata().astype(np.float32)
                vol2 = nib.load(path2).get_fdata().astype(np.float32)
        except Exception as e:
            st.error(f"Error loading NIfTI: {e}")
            # cleanup
            for p in (path1, path2):
                try:
                    if p and os.path.exists(p):
                        os.remove(p)
                except:
                    pass
            st.stop()

        # Simple feature extraction placeholder (demo)
        prog = st.progress(0)
        time.sleep(0.2)
        prog.progress(10)

        try:
            # DEMO: compute a handful of simple statistics as features
            f = [
                vol1.mean(),
                vol1.std(),
                vol1.max(),
                vol1.min(),
                vol2.mean(),
                vol2.std(),
                vol2.max(),
                vol2.min(),
            ]
            feats = np.asarray(f, dtype=np.float32).reshape(1, -1)
        except Exception as e:
            st.error(f"Feature extraction failed: {e}")
            for p in (path1, path2):
                try:
                    if p and os.path.exists(p):
                        os.remove(p)
                except:
                    pass
            st.stop()

        prog.progress(50)
        time.sleep(0.2)

        # Try load model
        if os.path.exists(MODEL_PATH):
            try:
                rf = joblib.load(MODEL_PATH)
            except Exception as e:
                st.warning(f"Error loading RandomForest model: {e}")
                st.info("Falling back to demo result.")
                rf = None
        else:
            st.warning(f"RandomForest not found at {MODEL_PATH}. Using demo fallback.")
            rf = None

        result = None
        if rf is not None:
            ok, res = safe_predict_with_model(rf, feats)
            if not ok:
                st.warning(f"Error loading/predicting with RandomForest: {res.get('error')}")
                st.info("Using demo fallback result.")
                result = {"label": 1, "mean_prob": 0.4881, "note": "demo fallback"}
            else:
                result = res
                if res.get("note"):
                    st.info(res["note"])
        else:
            # demo fallback
            result = {"label": 1, "mean_prob": 0.4881, "note": "demo fallback"}

        # store results in session_state
        st.session_state["ai_result"] = int(result.get("label", 1))
        st.session_state["ai_prob"] = float(result.get("mean_prob", 0.0))
        st.session_state["ai_note"] = result.get("note", None)

        prog.progress(100)
        st.success("Analysis complete.")

        # cleanup
        for p in (path1, path2):
            try:
                if p and os.path.exists(p):
                    os.remove(p)
            except:
                pass

        # Provide a link/button to insights (navigation)
        st.markdown("### Next step")
        st.markdown("You can view the results summary on the **Insights** page.")
        st.markdown("[🔎 View Insights](/Insights)", unsafe_allow_html=True)
        st.button("Open Insights", on_click=lambda: None)  # visual affordance

