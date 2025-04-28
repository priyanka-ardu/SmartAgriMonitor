import sys, os
import streamlit as st
import importlib

# Resolve project root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Page Config ──
st.set_page_config(
    page_title="Smart Agriculture Monitoring System",
    layout="wide"
)

# Get the page from the query parameter (or default to "1_upload_data")
page = st.query_params.get("page", ["1_upload_data"])[0]

# ── Page Navigation ──
if page == "1_upload_data":
    st.title("📥 Upload Data")
    # Dynamically import content from the 1_upload_data.py page
    module = importlib.import_module('pages.1_upload_data')
    module.main()

elif page == "2_eda":
    st.title("📊 Exploratory Data Analysis & Cleaning")
    # Dynamically import content from the 2_eda.py page
    module = importlib.import_module('pages.2_eda')
    module.main()

elif page == "3_clustering":
    st.title("🔍 Clustering")
    # Dynamically import content from the 3_clustering.py page
    module = importlib.import_module('pages.3_clustering')
    module.main()

elif page == "4_classification":
    st.title("📈 Classification")
    # Dynamically import content from the 4_classification.py page
    module = importlib.import_module('pages.4_classification')
    module.main()

elif page == "5_forecasting":
    st.title("📅 Forecasting")
    # Dynamically import content from the 5_forecasting.py page
    module = importlib.import_module('pages.5_forecasting')
    module.main()

elif page == "6_dashboard":
    st.title("📊 Dashboard")
    # Dynamically import content from the 6_dashboard.py page
    module = importlib.import_module('pages.6_dashboard')
    module.main()

else:
    st.title("Welcome to the Smart Agriculture Monitoring System")
    st.markdown("Please select a page from the navigation.")

# ── Navigation Button ──
st.sidebar.title("Navigation")
pages = [
    "1_upload_data",
    "2_eda",
    "3_clustering",
    "4_classification",
    "5_forecasting",
    "6_dashboard"
]
for page_option in pages:
    st.sidebar.button(f"Go to {page_option.replace('_', ' ').title()}", key=page_option, on_click=lambda p=page_option: st.experimental_set_query_params(page=p))
