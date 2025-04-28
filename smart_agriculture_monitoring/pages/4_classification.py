import sys, os
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Resolve project root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

st.title("🧠 Classification Model")

# ── Navigation function for manual page navigation ──
def navigate_to(page_name):
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

# ── Check for uploaded data ──
if 'df' not in st.session_state:
    st.warning("⚠️ No data loaded. Please go to **Page 1: Upload Data** first.")
    if st.button("⬅️ Go to Upload Page"):
        navigate_to("1_upload_data")
    st.stop()

df = st.session_state['df']

st.subheader("Select Features & Target Variable")

numeric_cols = df.select_dtypes(include='number').columns.tolist()
if len(numeric_cols) < 2:
    st.error("⚠️ Need at least 2 numeric columns for classification.")
    st.stop()

target = st.selectbox("Choose the target (label) column:", options=numeric_cols)

feature_options = [col for col in numeric_cols if col != target]
selected_features = st.multiselect(
    "Select feature columns:",
    options=feature_options,
    default=feature_options[:3]
)

if len(selected_features) < 1:
    st.info("👉 Please select at least one feature.")
    st.stop()

st.subheader("Train/Test Split Settings")
test_size = st.slider("Test set size (as %):", min_value=0.1, max_value=0.5, value=0.3)

if st.button("Run Classification"):
    X = df[selected_features].dropna()
    y = df[target].loc[X.index]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    st.success("✅ Classification Model Trained Successfully!")

    st.subheader("📊 Classification Report")
    report = classification_report(y_test, y_pred, output_dict=True)
    st.dataframe(pd.DataFrame(report).transpose())

    st.subheader("📊 Confusion Matrix")
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    st.pyplot(fig)

# ── Navigation Buttons ──
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Back to Clustering", key="back_to_clustering"):
        navigate_to("3_clustering")

with col2:
    if st.button("Proceed to Forecasting →", key="to_forecasting"):
        navigate_to("5_forecasting")
