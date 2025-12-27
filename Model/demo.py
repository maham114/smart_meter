# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from predictor import predict_energy

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="AI Smart Meter Advisor", page_icon="⚡", layout="wide")

# ----------------------------
# Neon Dark UI CSS
# ----------------------------
st.markdown("""
<style>
.stApp { background: #0B0F1A; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
h1,h2,h3,h4,h5,h6 { background: linear-gradient(135deg, #7F5AF0, #4D96FF);
                      -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.stDataFrameContainer div[data-testid="stVerticalBlock"] { background: rgba(255,255,255,0.05); border-radius:12px; padding:8px; }
.stDataFrameContainer th { background:#7F5AF0 !important; color:white !important; }
.stButton>button { background: linear-gradient(135deg, #7F5AF0, #4D96FF); color:white; border-radius:12px;
                   padding:8px 24px; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Hero Section
# ----------------------------
st.markdown("""
<h1 style='text-align:center;'>⚡ AI Smart Meter Advisor</h1>
<p style='text-align:center;'>Predict electricity usage using AI & ML</p>
<hr>
""", unsafe_allow_html=True)

# ----------------------------
# Load Predictions
# ----------------------------
hist_df, pred_df, avg_usage, ai_advice = predict_energy()

# ----------------------------
# Historical Data
# ----------------------------
st.subheader("📂 Historical Usage")
with st.expander("Click to view historical daily usage"):
    st.dataframe(hist_df[['Date_only','Daily_kWh','Usage_Type']], width='stretch')

# ----------------------------
# Key Metrics
# ----------------------------
st.subheader("📊 Key Insights")
col1, col2, col3 = st.columns(3)
col1.metric("⚡ Average Usage", f"{avg_usage:.2f} kWh")
peak_days = pred_df[pred_df["Usage_Type"]=="Peak"]
col2.metric("📈 Next Peak Day", str(peak_days.iloc[0]['Date'].date()) if not peak_days.empty else "No peak")
col3.metric("📅 Days Predicted", len(pred_df))

# ----------------------------
# Predicted Consumption Chart (Plotly)
# ----------------------------
st.subheader("📈 Predicted Electricity Consumption")

fig = px.line(
    pred_df,
    x="Date",
    y="Predicted_kWh",
    markers=True,
    title="7-Day Electricity Usage Forecast"
)

# 🔹 Add shaded area under the line
fig.update_traces(
    fill="tozeroy",                 # shade to x-axis
    fillcolor="rgba(127,90,240,0.25)",  # soft purple shade
    line=dict(width=3)
)

# 🔹 Dark theme styling
fig.update_layout(
    plot_bgcolor="#0B0F1A",
    paper_bgcolor="#0B0F1A",
    font_color="white",
    xaxis_title="Date",
    yaxis_title="Predicted kWh",
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)


# ----------------------------
# Prediction Table
# ----------------------------
st.subheader("📋 Upcoming 7-Day Usage")
st.dataframe(pred_df[['Date','Predicted_kWh','Usage_Type']], width='stretch')

# ----------------------------
# AI Advice Section
# ----------------------------
st.subheader("🤖 AI Energy Saving Plan")
with st.expander("Click to view AI-generated 7-day action plan"):
    st.text(ai_advice)
