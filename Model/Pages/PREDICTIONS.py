import streamlit as st
from ui import load_ui
from predictor import predict_energy_cached
import pandas as pd

load_ui()
hist_df, pred_df, avg_usage, ai_advice, forecast_explanation = predict_energy_cached()

st.markdown("<h1>📈 7-Day Predictions</h1>", unsafe_allow_html=True)

# Prediction Table
st.dataframe(pred_df[['Date','Predicted_kWh','Usage_Type']], width=900)
