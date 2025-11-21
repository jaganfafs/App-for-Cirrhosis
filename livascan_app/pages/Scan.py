import streamlit as st
import joblib
from utils import (
    save_uploaded_file,
    load_nifti,
    extract_features,
    compute_slice_distribution
)

st.title("Upload T1 & T2 MRI Scans")

uploaded_t1 = st.file_uploader("Upload T1 MRI", type=["nii", "nii.gz"])
uploaded_t2 = st.file_uploader("Upload T2 MRI", type=["nii", "nii.gz"])

if st.button("Start AI Analysis"):

    if not uploaded_t1 or not uploaded_t2:
        st.error("Please upload both T1 and T2 scans.")
        st.stop()

    t1_path = save_uploaded_file(uploaded_t1)
    t2_path = save_uploaded_file(uploaded_t2)

    vol1 = load_nifti(t1_path)
    vol2 = load_nifti(t2_path)

    if vol1 is None or vol2 is None:
        st.error("Error loading MRI scans")
        st.stop()

    # feature extraction (32×48 = 1536 features)
    f1 = extract_features(vol1)
    f2 = extract_features(vol2)

    if f1 is None or f2 is None:
        st.error("Could not extract features from MRI data")
        st.stop()

    features = (f1 + f2) / 2  # average both

    try:
        model = joblib.load("model/RandomForest_Cirrhosis.pkl")
        prediction = model.predict(features)[0]
    except Exception as e:
        st.warning(f"Model error: {e}")
        prediction = "Borderline"

    st.session_state["prediction"] = prediction

    # slice distribution for Report page
    h, c = compute_slice_distribution(vol1)
    st.session_state["slice_dist"] = {"healthy": h, "cirrhosis": c}

    st.success("Analysis complete! Redirecting...")
    st.switch_page("pages/Insights.py")

