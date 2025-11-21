# livascan_app/utils.py
import os
import tempfile
from pathlib import Path
import joblib
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent

def save_uploadedfile(uploaded_file, dst_folder=None):
    """
    Save a Streamlit uploaded_file (UploadedFile) to a temporary path and return the path.
    """
    if dst_folder is None:
        dst_folder = tempfile.gettempdir()
    os.makedirs(dst_folder, exist_ok=True)
    out_path = os.path.join(dst_folder, uploaded_file.name)
    # Write bytes to disk
    with open(out_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return out_path

def load_rf_model(model_rel_path="model/RandomForest_Cirrhosis.pkl"):
    """
    Try to load the RandomForest model. Return model or None + error string.
    """
    model_path = BASE_DIR / model_rel_path
    if not model_path.exists():
        return None, f"Model file not found at {model_path}"
    try:
        mdl = joblib.load(model_path)
        return mdl, None
    except Exception as e:
        return None, f"Error loading RF model: {e}"

def demo_result(n_slices):
    """
    Create a demo fallback result dict (used if RF model fails or incompatibility).
    """
    # simplistic simulated probabilities
    rng = np.random.RandomState(42)
    probs = rng.uniform(0.2, 0.8, size=n_slices)
    return probs

def bar_plot_counts(counts, labels=("Cirrhosis", "Healthy")):
    """
    Return a matplotlib figure with counts bar chart.
    counts: dict or sequence with two values
    """
    # Ensure sequence
    if isinstance(counts, dict):
        vals = [counts.get(labels[0], 0), counts.get(labels[1], 0)]
    else:
        vals = list(counts)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(labels, vals)
    ax.set_ylabel("Slices")
    ax.set_title("Slice-wise distribution")
    ax.set_ylim(0, max(1, max(vals) * 1.2))
    return fig

