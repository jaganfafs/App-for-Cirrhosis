# livascan_app/utils.py
import os
import tempfile
import nibabel as nib

ROOT = os.path.dirname(os.path.dirname(__file__))  # repo/livascan_app

def save_uploaded_file(uploaded_file, dest_folder=None):
    """
    Save a Streamlit UploadedFile to a temp path and return the file path.
    """
    if dest_folder is None:
        dest_folder = tempfile.gettempdir()
    os.makedirs(dest_folder, exist_ok=True)
    out_path = os.path.join(dest_folder, uploaded_file.name)
    # uploaded_file is a stream-like object - read and write bytes
    with open(out_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # safe and efficient
    return out_path

def load_nifti_from_uploaded(uploaded_file):
    """
    Save uploaded file to tmp and load as nibabel image.
    Returns numpy array (fdata).
    """
    path = save_uploaded_file(uploaded_file)
    img = nib.load(path)
    data = img.get_fdata().astype("float32")
    return data, path

def project_root():
    return ROOT
