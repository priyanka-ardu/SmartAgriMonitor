# src/pages/3_clustering.py

import sys, os
# # Resolve the project root (one level up from this pages/ folder)
# ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# # Add the project root to PYTHONPATH so `import src...` works
# sys.path.insert(0, ROOT)

# ── Ensure project root is on the path so we can import src.utils ──
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

# ── Page config ──
st.set_page_config(
    page_title="3. Clustering",
    page_icon="� clusters",
    layout="wide"
)

st.title("3. Unsupervised Clustering (K-Means)")

# ── Load the DataFrame ──
if "df" not in st.session_state:
    st.warning("⚠️ No data found. Please upload a dataset on **Page 1** first.")
    st.stop()

df: pd.DataFrame = st.session_state.df.copy()

# ── Select numeric features ──
numeric_cols = df.select_dtypes(include="number").columns.tolist()
if not numeric_cols:
    st.error("No numeric columns in data for clustering.")
    st.stop()

st.subheader("Select Features for Clustering")
features = st.multiselect(
    "Numeric columns:",
    options=numeric_cols,
    default=numeric_cols[:2]
)

if len(features) < 2:
    st.info("Please select at least two features.")
    st.stop()

# ── Choose number of clusters ──
n_clusters = st.slider("Number of clusters (k)", min_value=2, max_value=10, value=3)

# ── Run K-Means ──
if st.button("Run K-Means Clustering"):
    # Fit and predict
    km = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = km.fit_predict(df[features])

    # Persist clustered DataFrame
    st.session_state.df = df

    st.success(f"✅ K-Means completed with k={n_clusters}!")
    st.subheader("Cluster Counts")
    st.dataframe(df["cluster"].value_counts().sort_index(), use_container_width=True)

    # ── Show some cluster assignments ──
    st.subheader("Sample Cluster Assignments")
    st.dataframe(df[features + ["cluster"]].head(10), use_container_width=True)

    # ── Geospatial Map if lat/lon present ──
    if {"latitude", "longitude"}.issubset(df.columns):
        st.subheader("Map of Clusters")
        # Compute colors per cluster
        def color_for(x):
            ratio = x / (n_clusters - 1) if n_clusters > 1 else 0
            return [int(255 * ratio), int(255 * (1 - ratio)), 30]

        df["cluster_color"] = df["cluster"].apply(color_for)

        # Create PyDeck layer
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position="[longitude, latitude]",
            get_fill_color="cluster_color",
            pickable=True,
            radius_scale=10,
            radius_min_pixels=3,
        )
        view = pdk.ViewState(
            latitude=df["latitude"].mean(),
            longitude=df["longitude"].mean(),
            zoom=10,
            pitch=0,
        )
        deck = pdk.Deck(layers=[layer], initial_view_state=view)
        st.pydeck_chart(deck)
    else:
        # ── 2D Scatter Plot ──
        st.subheader("2D Scatter Plot of First Two Features")
        fig, ax = plt.subplots()
        sns.scatterplot(
            x=features[0],
            y=features[1],
            hue="cluster",
            palette="tab10",
            data=df,
            ax=ax,
            legend="full"
        )
        ax.set_title(f"K-Means Clusters (k={n_clusters})")
        st.pyplot(fig)

    st.markdown(
        """
        ---
        **Next:** Proceed to **Page 4: Stress Classification** in the sidebar.
        """
    )
else:
    st.info("Click **Run K-Means Clustering** to segment your data into zones.")
