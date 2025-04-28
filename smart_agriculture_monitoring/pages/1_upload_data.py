import sys, os
import streamlit as st
import pandas as pd
import glob

# Resolve project root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.utils.data_loader import load_data
import kagglehub  # optional, if you're using kagglehub

st.title("📥 Upload or Download Your Dataset")
st.markdown("""
Upload a CSV/Excel file of your data **or download a sample from Kaggle**.
""")

# ── Section A: File Uploader ──
st.subheader("A. Upload CSV/Excel File")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xls", "xlsx"]
)

def navigate_to(page_name):
    """Navigate to another page by setting the page query param."""
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

if uploaded_file:
    df = load_data(uploaded_file)
    if df is None:
        st.error("🚨 Could not load the file. Make sure it’s a valid CSV/XLSX.")
    else:
        st.success("✅ Data loaded successfully!")
        st.session_state['df'] = df

        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head(), use_container_width=True)

        # Navigate to EDA & Cleaning when the button is clicked
        if st.button("Go to EDA & Cleaning →", key="nav_upload"):
            navigate_to("2_eda")

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
        st.error("Please select a dataset.")
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
                    st.error("No CSV files found.")
                else:
                    df_sample = pd.read_csv(csv_files[0])
                    st.session_state['df'] = df_sample

                    st.subheader("Preview of Sample Data")
                    st.dataframe(df_sample.head(), use_container_width=True)

                    # Navigate to EDA & Cleaning when the button is clicked
                    if st.button("Go to EDA & Cleaning →", key="nav_kaggle"):
                        navigate_to("2_eda")

            except Exception as e:
                st.error(f"Failed to download dataset: {e}")
