# pages/2_eda.py
import sys, os
# Resolve the project root (one level up from this pages/ folder)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the project root to PYTHONPATH so `import src...` works
sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
from smart_agriculture_monitoring.src.utils.sample_data_loader import check_missing_values, get_basic_stats

# --- Page Config ---
st.set_page_config(
    page_title="2. EDA & Cleaning",
    page_icon="📊",
    layout="wide"
)

st.title("2. Exploratory Data Analysis & Cleaning")

# --- Load DataFrame from session_state ---
if "df" not in st.session_state:
    st.warning("⚠️ No data loaded. Please go to **Upload Data** (Page 1) and upload a CSV/Excel file first.")
    st.stop()

df: pd.DataFrame = st.session_state.df

# --- Basic Statistics ---
st.header("Dataset Overview")
stats = get_basic_stats(df)

st.subheader("First 5 Rows")
st.dataframe(stats["head"], use_container_width=True)

st.subheader("Data Types & Info")
st.text(stats["info"])

st.subheader("Descriptive Statistics")
st.dataframe(stats["describe"].T, use_container_width=True)

# --- Missing Values ---
st.header("Missing Value Analysis")
missing = check_missing_values(df)
st.bar_chart(missing)

# --- Missing Value Handling ---
st.subheader("Handle Missing Values")
strategy = st.radio(
    "Choose a strategy to handle missing values:",
    options=["Drop rows with missing", "Fill with mean (numeric)", "Fill with median (numeric)"]
)

if st.button("Apply Missing-Value Strategy"):
    if strategy == "Drop rows with missing":
        df_clean = df.dropna()
    elif strategy == "Fill with mean (numeric)":
        df_clean = df.fillna(df.mean(numeric_only=True))
    else:
        df_clean = df.fillna(df.median(numeric_only=True))

    st.session_state.df = df_clean
    st.success(f"✅ Missing values handled using **{strategy}**.")
    st.experimental_rerun()

# --- Outlier Detection via IQR ---
st.header("Outlier Detection (IQR Method)")
numeric_cols = df.select_dtypes(include="number").columns.tolist()

if numeric_cols:
    col = st.selectbox("Select numeric column to inspect for outliers:", numeric_cols)

    if col:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        mask = (df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))
        outliers = df[mask]

        st.write(f"🔎 Found **{len(outliers)}** outliers in **{col}**")
        st.dataframe(outliers, use_container_width=True)

        if st.button("Remove Outliers"):
            df_no_out = df[~mask]
            st.session_state.df = df_no_out
            st.success("✅ Outliers removed.")
            st.experimental_rerun()
else:
    st.info("No numeric columns found for outlier detection.")

# --- Feature Engineering: Rolling Averages ---
st.header("Feature Engineering: Rolling Averages")
window = st.slider("Rolling window size:", min_value=2, max_value=30, value=7)

if st.button("Compute Rolling Averages"):
    df_feat = df.copy()
    for c in numeric_cols:
        df_feat[f"{c}_rolling_{window}"] = df_feat[c].rolling(window).mean()
    st.session_state.df = df_feat
    st.success(f"✅ Rolling averages (window={window}) added as new columns.")
    st.experimental_rerun()

st.markdown("---")
st.info("When you're satisfied with your cleaned & enriched dataset, move on to **Page 3: Clustering**.")