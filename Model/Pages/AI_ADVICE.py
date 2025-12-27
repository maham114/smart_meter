import streamlit as st
from ui import load_ui
from predictor import predict_energy_cached

load_ui()
hist_df, pred_df, avg_usage, ai_advice, forecast_explanation = predict_energy_cached()

st.markdown("<h1>🤖 AI Energy Saving Tips</h1>", unsafe_allow_html=True)

# Show AI advice in cards
cols = st.columns(3)
for i, row in pred_df.iterrows():
    date_str = row["Date"].strftime("%Y-%m-%d")
    tip = ai_advice.get(date_str, "Use electricity efficiently today.")
    with cols[i%3]:
        st.markdown(f"""
        <div class="advice-card advice-indigo">
            <div class="advice-title">📅 {row['Date'].strftime('%A, %b %d')}</div>
            <div>{tip}</div>
        </div>
        """, unsafe_allow_html=True)
