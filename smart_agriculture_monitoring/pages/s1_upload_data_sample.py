# src/pages/1_upload_data.py

# src/pages/1_upload_data.py

import sys, os
# Resolve the project root (one level up from this pages/ folder)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the project root to PYTHONPATH so `import src...` works
sys.path.insert(0, ROOT)


# ── Add project root to sys.path so `import src.utils` works ──
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# src/pages/1_upload_data.py

import streamlit as st
import pandas as pd
import glob
import kagglehub  # or replace with KaggleApi if you switched

from smart_agriculture_monitoring.src.utils.sample_data_loader import load_data

# ── Page Configuration ──
st.set_page_config(
    page_title="1. Upload Data",
    page_icon="📥",
    layout="wide"
)

st.title("1. Upload Your Dataset")
st.markdown(
    """
    You can either **upload** your own CSV/Excel file,
    or **download** a sample directly from Kaggle.
    """
)

def navigate_to_eda():
    """Use JS to redirect browser to Page 2 (2_eda)."""
    js = """
    <script>
      // Redirect to the multipage route for Page 2
      window.location.href = "pages/2_eda.py";
    </script>
    """
    st.markdown(js, unsafe_allow_html=True)
    # No need for rerun; JS navigation takes over

# ── Section A: File Uploader ──
st.subheader("A. Upload CSV/Excel File")
uploaded_file = st.file_uploader(
    label="Choose a CSV or Excel file",
    type=["csv", "xls", "xlsx"]
)

if uploaded_file:
    df = load_data(uploaded_file)
    if df is None:
        st.error("🚨 Failed to load the file. Please ensure it’s a valid CSV/XLSX.")
    else:
        st.success("✅ Data loaded successfully!")
        st.session_state.df = df

        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head(), use_container_width=True)

        # Navigation button
        if st.button("Go to EDA & Cleaning →", key="nav_upload"):
            navigate_to_eda()

st.markdown("---")

# ── Section B: Download Sample from Kaggle ──
st.subheader("B. Download Sample Dataset from Kaggle")

dataset_option = st.selectbox(
    "Choose a sample to download:",
    [
        "Select…",
        "NDVI (humaishassan/csv-files-with-ndvi)",
        "Crop Yield (patelris/crop-yield-prediction-dataset)"
    ]
)

if st.button("Download from Kaggle", key="kaggle_download"):
    if dataset_option == "Select…":
        st.error("Please select a dataset from the dropdown.")
    else:
        mapping = {
            "NDVI (humaishassan/csv-files-with-ndvi)": "humaishassan/csv-files-with-ndvi",
            "Crop Yield (patelris/crop-yield-prediction-dataset)": "patelris/crop-yield-prediction-dataset"
        }
        dataset_id = mapping[dataset_option]

        with st.spinner(f"Downloading {dataset_id}…"):
            try:
                path = kagglehub.dataset_download(dataset_id)
                st.success(f"✅ Downloaded to `{path}`")

                csv_files = glob.glob(os.path.join(path, "*.csv"))
                if not csv_files:
                    st.error("No CSV files found in the downloaded dataset.")
                else:
                    df_sample = pd.read_csv(csv_files[0])
                    st.session_state.df = df_sample

                    st.subheader("Preview of Kaggle Sample Data")
                    st.dataframe(df_sample.head(), use_container_width=True)

                    # Navigation button
                    if st.button("Go to EDA & Cleaning →", key="nav_kaggle"):
                        navigate_to_eda()

            except Exception as e:
                st.error(f"Failed to download or load dataset: {e}")
