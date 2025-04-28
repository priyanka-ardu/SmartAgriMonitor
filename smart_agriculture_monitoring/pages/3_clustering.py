import sys, os
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Resolve project root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Navigation function for manual page navigation
def navigate_to(page_name):
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

st.title("📊 Clustering Analysis")

# ── Check for uploaded data ──
if 'df' not in st.session_state:
    st.warning("⚠️ No data loaded. Please go to **Page 1: Upload Data** first.")
    if st.button("⬅️ Go to Upload Page"):
        navigate_to("1_upload_data")
    st.stop()

df = st.session_state['df']

st.subheader("Select Features for Clustering")

numeric_cols = df.select_dtypes(include='number').columns.tolist()
if len(numeric_cols) < 2:
    st.error("⚠️ Need at least 2 numeric columns for clustering.")
    st.stop()

selected_features = st.multiselect(
    "Choose numeric columns for clustering:",
    options=numeric_cols,
    default=numeric_cols[:2]
)

if len(selected_features) < 2:
    st.info("👉 Please select at least two features.")
    st.stop()

X = df[selected_features].dropna()

st.subheader("Choose Number of Clusters (K)")
k = st.slider("Select number of clusters:", min_value=2, max_value=10, value=3)

if st.button("Run Clustering"):
    model = KMeans(n_clusters=k, random_state=42)
    df['Cluster'] = model.fit_predict(X)

    st.session_state.df = df  # Update state with cluster labels
    st.success(f"✅ Clustering done with {k} clusters.")

    # Visualize Clusters
    st.subheader("Cluster Visualization")

    if len(selected_features) >= 2:
        fig, ax = plt.subplots()
        sns.scatterplot(
            data=df,
            x=selected_features[0],
            y=selected_features[1],
            hue='Cluster',
            palette="viridis",
            ax=ax
        )
        ax.set_title("Clusters by Selected Features")
        st.pyplot(fig)
    else:
        st.warning("Visualization needs at least 2 numeric features.")

# ── Navigation Buttons ──
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Back to EDA", key="back_to_eda"):
        navigate_to("2_eda")

with col2:
    if st.button("Proceed to Classification →", key="to_classification"):
        navigate_to("4_classification")
