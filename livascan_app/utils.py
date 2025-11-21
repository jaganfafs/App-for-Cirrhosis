import numpy as np
import nibabel as nib
import os
import tempfile
from skimage.transform import resize

# ---------------------------
# Save UploadedFile to temp
# ---------------------------
def save_uploaded_file(uploaded_file):
    """Save uploaded Streamlit file to a temporary path."""
    if uploaded_file is None:
        return None
    suffix = uploaded_file.name.split(".")[-1]
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix="." + suffix)
    temp_file.write(uploaded_file.getvalue())
    temp_file.close()
    return temp_file.name

# ---------------------------
# Load NIfTI safely
# ---------------------------
def load_nifti(path):
    try:
        return nib.load(path).get_fdata()
    except Exception as e:
        print(f"Error loading NIFTI: {e}")
        return None

# --------------------------------------
# Extract a SINGLE feature vector (1536)
# --------------------------------------
def extract_features(volume, target_size=(32, 48)):
    """
    Resize each slice to 32×48 and flatten → 1536 features.
    Use only the middle slice.
    """
    if volume is None:
        return None

    mid_slice = volume[:, :, volume.shape[2] // 2]
    mid_slice = resize(mid_slice, target_size, anti_aliasing=True)
    return mid_slice.flatten().reshape(1, -1)

# ---------------------------
# Slice distribution
# ---------------------------
def compute_slice_distribution(volume):
    """Return dummy healthy/cirrhotic distribution since RF model is slice-based."""
    total = volume.shape[2]
    healthy = int(total * 0.70)
    cirrhosis = total - healthy
    return healthy, cirrhosis

