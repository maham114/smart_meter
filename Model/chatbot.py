# chatbot.py
import requests
import os
import pandas as pd

API_URL = "https://router.huggingface.co/v1/chat/completions"

def energy_chatbot(user_question, hist_df, pred_df, avg_usage):

    # -----------------------------
    # Build Context from Data
    # -----------------------------
    peak_days = pred_df[pred_df["Usage_Type"] == "Peak"]
    next_peak = (
        peak_days.iloc[0]["Date"].strftime("%Y-%m-%d")
        if not peak_days.empty else "No peak expected"
    )

    forecast_summary = ""
    for _, row in pred_df.iterrows():
        forecast_summary += (
            f"{row['Date'].strftime('%Y-%m-%d')}: "
            f"{row['Predicted_kWh']:.1f} kWh ({row['Usage_Type']})\n"
        )

    context = f"""
You are an AI energy assistant.

Here is the household electricity data summary:

- Average daily consumption: {avg_usage:.2f} kWh
- Next predicted peak day: {next_peak}

7-day forecast:
{forecast_summary}

Rules:
- Answer ONLY using this data
- If data is insufficient, say "Based on available data, this cannot be determined"
- Be concise, practical, and user-friendly
- Assume Pakistani household context
"""

    # -----------------------------
    # LLM Call
    # -----------------------------
    payload = {
        "model": "deepseek-ai/DeepSeek-V3.2:novita",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": user_question}
        ],
        "max_tokens": 300
    }

    headers = {
        "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "⚠️ Unable to fetch response right now."
    except Exception:
        return "⚠️ Chatbot service unavailable."
