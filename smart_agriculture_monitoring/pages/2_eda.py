import sys, os
import streamlit as st
import pandas as pd

# Resolve project root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.utils.data_loader import check_missing_values, get_basic_stats

# Navigation function
def navigate_to(page_name):
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

st.title("📊 Exploratory Data Analysis & Cleaning")

# ── Check for uploaded data ──
if 'df' not in st.session_state:
    st.warning("⚠️ No data loaded. Please go to **Page 1: Upload Data** first.")
    if st.button("⬅️ Go to Upload Page"):
        navigate_to("1_upload_data")
    st.stop()

df = st.session_state['df']

st.subheader("Preview of Data")
st.dataframe(df.head(), use_container_width=True)

# ── Basic Stats ──
st.subheader("📈 Basic Data Statistics")
stats_df = get_basic_stats(df)
st.dataframe(stats_df, use_container_width=True)

# ── Missing Value Check ──
st.subheader("🕳️ Missing Value Check")
missing_df = check_missing_values(df)
st.dataframe(missing_df, use_container_width=True)

# ── Navigation Buttons ──
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Back to Upload", key="back_to_upload"):
        navigate_to("1_upload_data")

with col2:
    if st.button("Proceed to Clustering →", key="to_clustering"):
        navigate_to("3_clustering")
