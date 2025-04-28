import sys, os
import streamlit as st
import pandas as pd
import plotly.express as px

# Resolve project root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

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

# ── Dashboard Overview ──
st.title("📊 Dashboard")

st.subheader("Data Overview")

if st.checkbox("Show Data", value=True):
    st.dataframe(df)

st.subheader("Exploratory Data Analysis")

# Choose column for analysis
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if len(numerical_columns) > 0:
    selected_column = st.selectbox("Select a numerical column to analyze", options=numerical_columns)

    if selected_column:
        st.subheader(f"Distribution of {selected_column}")
        fig = px.histogram(df, x=selected_column, title=f"Distribution of {selected_column}")
        st.plotly_chart(fig)

        st.subheader(f"Boxplot of {selected_column}")
        fig_box = px.box(df, y=selected_column, title=f"Boxplot of {selected_column}")
        st.plotly_chart(fig_box)

else:
    st.warning("⚠️ No numerical columns available for EDA.")

# ── Correlation Heatmap ──
st.subheader("Correlation Heatmap")
if len(numerical_columns) > 0:
    correlation_matrix = df[numerical_columns].corr()
    fig_corr = px.imshow(correlation_matrix, title="Correlation Heatmap", color_continuous_scale='Blues')
    st.plotly_chart(fig_corr)
else:
    st.warning("⚠️ No numerical columns available for correlation analysis.")

# ── Clustering Visualizations ──
st.subheader("Clustering Results")
# Assuming clustering results are available in the dataframe, e.g., 'Cluster' column
if 'Cluster' in df.columns:
    st.write("Displaying clustering results based on 'Cluster' column.")
    fig_cluster = px.scatter(df, x=numerical_columns[0], y=numerical_columns[1], color='Cluster', title="Clustering Visualization")
    st.plotly_chart(fig_cluster)
else:
    st.write("Clustering not yet performed. Please go to **Page 3: Clustering** to perform clustering.")

# ── Forecasting Results ──
st.subheader("Forecasting Results")
# Assuming forecasting results are stored in session state after ARIMA or LSTM model runs
if 'forecast' in st.session_state:
    forecast = st.session_state['forecast']
    st.write("Displaying forecast results.")
    fig_forecast = px.line(forecast, title="Forecasted Values")
    st.plotly_chart(fig_forecast)
else:
    st.write("No forecast data available. Please go to **Page 5: Forecasting** to perform forecasting.")

# ── Navigation Buttons ──
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Back to Forecasting", key="back_to_forecasting"):
        navigate_to("5_forecasting")

with col2:
    if st.button("Finish and Save Results", key="finish_results"):
        st.write("Thank you for using the Smart Agriculture Monitoring System!")
        # Optionally, you can add code to save the results to a file or database here.
