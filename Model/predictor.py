# predictor.py
import pandas as pd
import numpy as np
import requests
import os
from sklearn.ensemble import RandomForestRegressor
from dotenv import load_dotenv

# -----------------------------
# Config
# -----------------------------
from dotenv import dotenv_values

config = dotenv_values(r"C:\Users\Administrator\Downloads\SMART METER HACKATHON WORK\AI SMART METER ADVISOR\Model\token.env")
HF_TOKEN = config.get("HF_TOKEN")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "energy_data.csv")

# -----------------------------
# Data Loading
# -----------------------------
def load_and_prepare_data():
    df = pd.read_csv(DATA_PATH, sep=';', low_memory=False)

    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], dayfirst=True)
    df.drop(columns=['Date', 'Time'], inplace=True)

    numeric_columns = [
        'Global_active_power', 'Global_reactive_power',
        'Voltage', 'Global_intensity',
        'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col].fillna(df[col].mean(), inplace=True)

    df = df[df['Global_active_power'] > 0]

    df['Date_only'] = df['DateTime'].dt.date
    df['Energy_kWh'] = df['Global_active_power'] / 60

    daily_usage = (
        df.groupby('Date_only')['Energy_kWh']
        .sum()
        .reset_index()
        .rename(columns={'Energy_kWh': 'Daily_kWh'})
    )

    return daily_usage

# -----------------------------
# Main Prediction Function
# -----------------------------

import streamlit as st

@st.cache_data(ttl=3600)  # cache results for 1 hour
def predict_energy_cached():
    from predictor import predict_energy
    return predict_energy()

def predict_energy():
    # -----------------------------
    # Load historical usage
    # -----------------------------
    daily_usage = load_and_prepare_data()
    avg_usage = daily_usage['Daily_kWh'].mean()

    daily_usage['Usage_Type'] = daily_usage['Daily_kWh'].apply(
        lambda x: 'Peak' if x > avg_usage else 'Normal'
    )

    # -----------------------------
    # Train model
    # -----------------------------
    daily_usage = daily_usage.sort_values('Date_only')
    daily_usage['Day_Num'] = np.arange(len(daily_usage))

    X = daily_usage[['Day_Num']]
    y = daily_usage['Daily_kWh']

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X, y)

    # -----------------------------
    # Predict next 7 days
    # -----------------------------
    last_day = daily_usage['Day_Num'].iloc[-1]
    future_days = np.arange(last_day + 1, last_day + 8).reshape(-1, 1)
    future_predictions = model.predict(future_days)
    future_predictions += np.random.normal(
        0, daily_usage['Daily_kWh'].std() * 0.05, size=future_predictions.shape
    )

    future_dates = pd.date_range(
        start=pd.to_datetime(daily_usage['Date_only'].iloc[-1]) + pd.Timedelta(days=1),
        periods=7
    )

    prediction_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted_kWh': future_predictions
    })

    prediction_df['Usage_Type'] = prediction_df['Predicted_kWh'].apply(
        lambda x: 'Peak' if x > avg_usage else 'Normal'
    )

    # -----------------------------
    # Generate LLM advice per day
    # -----------------------------
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}", "Content-Type": "application/json"}

    advice_dict = {}
    for _, row in prediction_df.iterrows():
        date_str = row['Date'].strftime("%Y-%m-%d")
        single_day_prompt = f"""
You are a professional home energy advisor.

Date: {date_str}
Predicted usage: {row['Predicted_kWh']:.1f} kWh ({row['Usage_Type']})

Task:
- Provide exactly 3 unique energy-saving tips for this day
- Each tip: 8–14 words, realistic household actions/appliances
- Format: Advice 1; Advice 2; Advice 3
- Do NOT repeat tips across other days
- No emojis, no extra text
"""
        payload = {
            "model": "deepseek-ai/DeepSeek-V3.2:novita",
            "messages": [{"role": "user", "content": single_day_prompt}],
            "max_tokens": 100,
            "temperature": 0.8,
            "top_p": 0.9
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                advice_dict[date_str] = content.strip()
            else:
                raise Exception("LLM error")
        except Exception:
            # Fallback generic tips
            generic_peak = [
                "Turn off unused appliances",
                "Avoid peak hour usage",
                "Use energy-efficient lights",
                "Run dishwasher only when full",
                "Unplug chargers when not needed"
            ]
            generic_normal = [
                "Maintain efficient energy habits",
                "Check for unnecessary loads",
                "Use natural light during daytime",
                "Lower heating/cooling slightly",
                "Run laundry in off-peak hours"
            ]
            tips = generic_peak if row['Usage_Type'] == "Peak" else generic_normal
            advice_dict[date_str] = "; ".join(np.random.choice(tips, 3, replace=False))

    # -----------------------------
    # Generate forecast explanation
    # -----------------------------
    forecast_explanation = generate_forecast_explanation(prediction_df)

    return daily_usage, prediction_df, avg_usage, advice_dict, forecast_explanation

# -----------------------------
# Forecast Explanation Function
# -----------------------------
def generate_forecast_explanation(pred_df):
    forecast_summary = ""
    for _, row in pred_df.iterrows():
        day_name = row['Date'].strftime("%A")
        date_str = row['Date'].strftime("%Y-%m-%d")
        kwh = round(row['Predicted_kWh'], 1)
        usage_type = row['Usage_Type']
        forecast_summary += f"{date_str} ({day_name}): {kwh} kWh ({usage_type})\n"

    prompt = f"""
You are an energy advisor explaining electricity forecasts to a household user.

Here is the upcoming 7-day electricity forecast:
{forecast_summary}

Write a clear and friendly summary (5–7 sentences):
- Describe overall energy consumption trend
- Mention which days may feel heavier
- Explain possible reasons (appliances or habits)
- Suggest general behavior improvements
- Do NOT list tips explicitly
"""

    API_URL = "https://router.huggingface.co/v1/chat/completions"
    headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}", "Content-Type": "application/json"}
    payload = {"model": "deepseek-ai/DeepSeek-V3.2:novita", "messages": [{"role": "user", "content": prompt}], "max_tokens": 150}

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            ai_response = response.json()
            explanation = ai_response["choices"][0]["message"]["content"] if "choices" in ai_response else "This week's forecast is ready."
        else:
            explanation = "This week's forecast is ready. Monitor your usage daily and try to save energy on peak days."
    except Exception:
        explanation = "This week's forecast is ready. Monitor your usage daily and try to save energy on peak days."

    return explanation
