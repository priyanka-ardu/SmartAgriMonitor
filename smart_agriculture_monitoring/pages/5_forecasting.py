import sys, os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np

# Resolve project root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ── Page Content ──
st.title("📉 Forecasting Model")

# ── Check for uploaded data ──
if 'df' not in st.session_state:
    st.warning("⚠️ No data loaded. Please go to **Page 1: Upload Data** first.")

    # Add a button to navigate manually using st.experimental_set_query_params()
    if st.button("⬅️ Go to Upload Page"):
        st.experimental_set_query_params(page="1_upload_data")
        st.experimental_rerun()  # Ensure page refreshes with the updated URL
    st.stop()

df = st.session_state['df']

st.subheader("Select Time Series Column for Forecasting")
time_series_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

if len(time_series_columns) == 0:
    st.error("⚠️ No numeric columns available for forecasting.")
    st.stop()

time_column = st.selectbox("Choose the time column (if applicable):", options=df.columns.tolist())

selected_feature = st.selectbox("Select the feature to forecast:", options=time_series_columns)

# ── ARIMA or LSTM Model ──
model_choice = st.radio("Select the Forecasting Model", options=["ARIMA", "LSTM"])

# ── Prepare Data for Forecasting ──
st.subheader("Data Preparation")

if st.button("Prepare Data"):
    if time_column and selected_feature:
        df_sorted = df.sort_values(time_column)
        df_sorted = df_sorted[[time_column, selected_feature]].dropna()

        if model_choice == "ARIMA":
            st.success(f"ARIMA Model Preparation Completed for {selected_feature}")
            # ARIMA requires a single feature column and time index
            ts = df_sorted[selected_feature]
            model = ARIMA(ts, order=(5, 1, 0))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=30)

            st.subheader(f"ARIMA Forecast for {selected_feature}")
            st.line_chart(forecast)
            st.write(forecast)

        elif model_choice == "LSTM":
            st.success(f"LSTM Model Preparation Completed for {selected_feature}")
            # Normalize the feature
            scaler = StandardScaler()
            df_sorted[selected_feature] = scaler.fit_transform(df_sorted[[selected_feature]])

            # Prepare data for LSTM
            window_size = 60
            X_data, y_data = [], []

            for i in range(window_size, len(df_sorted)):
                X_data.append(df_sorted[selected_feature][i-window_size:i].values)
                y_data.append(df_sorted[selected_feature][i])

            X_data, y_data = np.array(X_data), np.array(y_data)
            X_data = X_data.reshape((X_data.shape[0], X_data.shape[1], 1))

            # Build LSTM model
            model = Sequential()
            model.add(LSTM(units=50, return_sequences=True, input_shape=(X_data.shape[1], 1)))
            model.add(LSTM(units=50, return_sequences=False))
            model.add(Dense(units=1))
            model.compile(optimizer='adam', loss='mean_squared_error')

            # Fit model
            model.fit(X_data, y_data, epochs=1, batch_size=32)

            # Forecast
            forecast = model.predict(X_data[-30:].reshape(1, -1, 1))

            st.subheader(f"LSTM Forecast for {selected_feature}")
            st.line_chart(forecast.flatten())

# ── Navigation Buttons ──
col1, col2 = st.columns(2)

with col1:
    # Back to Classification Page (Page 4)
    if st.button("⬅️ Back to Classification", key="back_to_classification"):
        st.experimental_set_query_params(page="4_classification")
        st.experimental_rerun()

with col2:
    # Proceed to Dashboard Page (Page 6)
    if st.button("Proceed to Dashboard →", key="to_dashboard"):
        st.experimental_set_query_params(page="6_dashboard")
        st.experimental_rerun()
