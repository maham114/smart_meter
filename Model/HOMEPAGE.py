# # app.py
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from predictor import predict_energy



# # ----------------------------
# # Page Config
# # ----------------------------
# st.set_page_config(page_title="AI Smart Meter Advisor", page_icon="⚡", layout="wide")

# # ----------------------------
# # Neon Dark UI CSS
# # ----------------------------
# st.markdown("""
# <style>
# .stApp { background: #0B0F1A; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
# h1,h2,h3,h4,h5,h6 { background: linear-gradient(135deg, #7F5AF0, #4D96FF);
#                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
# .stDataFrameContainer div[data-testid="stVerticalBlock"] { background: rgba(255,255,255,0.05); border-radius:12px; padding:8px; }
# .stDataFrameContainer th { background:#7F5AF0 !important; color:white !important; }
# .stButton>button { background: linear-gradient(135deg, #7F5AF0, #4D96FF); color:white; border-radius:12px;
#                    padding:8px 24px; font-weight:bold; }

# .neon-card {
#     background: #0B0F1A;
#     border-radius: 15px;
#     padding: 20px;
#     text-align: center;
#     box-shadow: 0 0 20px rgba(127,90,240,0.6);
#     transition: 0.3s;
# }
# .neon-card:hover {
#     box-shadow: 0 0 40px rgba(127,90,240,0.8);
# }
# .neon-icon {
#     font-size: 40px;
#     color: #7F5AF0;
#     text-shadow: 0 0 10px #7F5AF0, 0 0 20px #7F5AF0;
# }
# .neon-text {
#     font-size: 20px;
#     color: white;
#     margin-top: 10px;
# }
# </style>
# """, unsafe_allow_html=True)

# # ----------------------------
# # Hero Section
# # ----------------------------
# st.markdown("""
# <h1 style='text-align:center;'>⚡ AI Smart Meter Advisor</h1>
# <p style='text-align:center;'>Predict electricity usage using AI & ML</p>
# <hr>
# """, unsafe_allow_html=True)

# # ----------------------------
# # Load Predictions
# # ----------------------------
# #hist_df, pred_df, avg_usage, ai_advice = predict_energy()
# hist_df, pred_df, avg_usage, ai_advice, forecast_explanation = predict_energy()

# # ----------------------------
# # Historical Data
# # ----------------------------
# st.subheader("📂 Historical Usage")
# with st.expander("Click to view historical daily usage"):
#     st.dataframe(hist_df[['Date_only','Daily_kWh','Usage_Type']], width='stretch')

# # ----------------------------
# # Key Metrics (Neon Glow Cards)
# # ----------------------------
# st.subheader("📊 Key Insights")

# peak_days = pred_df[pred_df["Usage_Type"]=="Peak"]
# next_peak = str(peak_days.iloc[0]['Date'].date()) if not peak_days.empty else "No peak"
# monthly_estimate = avg_usage * 30

# col1, col2, col3 = st.columns(3)
# col1.markdown(f"""
# <div class="neon-card">
#     <div class="neon-icon">⚡</div>
#     <div class="neon-text">Average Usage<br>{avg_usage:.2f} kWh/day</div>
# </div>
# """, unsafe_allow_html=True)

# col2.markdown(f"""
# <div class="neon-card">
#     <div class="neon-icon">📈</div>
#     <div class="neon-text">Next Peak Day<br>{next_peak}</div>
# </div>
# """, unsafe_allow_html=True)

# col3.markdown(f"""
# <div class="neon-card">
#     <div class="neon-icon">📅</div>
#     <div class="neon-text">Days Predicted<br>{len(pred_df)}</div>
# </div>
# """, unsafe_allow_html=True)

# # Extra card for monthly estimate
# st.markdown(f"""
# <div class="neon-card" style="margin-top:20px;">
#     <div class="neon-icon">💡</div>
#     <div class="neon-text">Estimated Monthly Consumption<br>{monthly_estimate:.1f} kWh</div>
# </div>
# """, unsafe_allow_html=True)

# # ----------------------------
# # Predicted Consumption Chart (Plotly)
# # ----------------------------
# st.subheader("📈 Predicted Electricity Consumption")

# fig = px.line(
#     pred_df,
#     x="Date",
#     y="Predicted_kWh",
#     markers=True,
#     title="7-Day Electricity Usage Forecast"
# )
# fig.update_traces(
#     fill="tozeroy",
#     fillcolor="rgba(127,90,240,0.25)",
#     line=dict(width=3)
# )
# fig.update_layout(
#     plot_bgcolor="#0B0F1A",
#     paper_bgcolor="#0B0F1A",
#     font_color="white",
#     xaxis_title="Date",
#     yaxis_title="Predicted kWh",
#     title_x=0.5
# )
# st.plotly_chart(fig, use_container_width=True)


# # ----------------------------
# # Forecast Explanation (Friendly)
# # ----------------------------
# st.subheader("📝 This Week's Forecast Summary")
# st.markdown(f"""
# <div style="color:white; font-size:16px; background: rgba(255,255,255,0.05); padding:12px; border-radius:12px;">
# {forecast_explanation}
# </div>
# """, unsafe_allow_html=True)


# # Prediction Table
# st.subheader("📋 Upcoming 7-Day Usage")
# st.dataframe(pred_df[['Date','Predicted_kWh','Usage_Type']], width='stretch')

# # ----------------------------
# # AI Advice Section
# # ----------------------------
# #st.subheader("🤖 AI Energy Saving Plan")
# #with st.expander("Click to view AI-generated 7-day action plan"):
# #   st.text(ai_advice)
# # ----------------------------
# # AI Advice Cards
# # ----------------------------
# st.markdown("""
# <style>
# .advice-card {
#     background: rgba(255,255,255,0.06);
#     padding: 16px;
#     border-radius: 14px;
#     margin-bottom: 14px;
#     transition: 0.3s ease;
#     border-left: 4px solid #7F5AF0;
#     box-shadow: 0 0 12px rgba(127,90,240,0.35);
# }
# .advice-card:hover {
#     background: rgba(127,90,240,0.25);
#     transform: translateY(-4px);
#     box-shadow: 0 0 22px rgba(127,90,240,0.6);
# }
# .day-title {
#     font-weight: bold;
#     margin-bottom: 6px;
#     color: #7F5AF0;
#     font-size: 16px;
# }
# </style>
# """, unsafe_allow_html=True)

# # Split AI advice into lines
# advice_dict = ai_advice
# st.subheader("🤖 AI Energy Saving Plan")

# cols = st.columns(3)

# for i, row in pred_df.iterrows():
#     date_str = row["Date"].strftime("%Y-%m-%d")
#     day_name = row["Date"].strftime("%A")
#     tip = advice_dict.get(date_str, "Use electricity efficiently today.")

#     with cols[i % 3]:
#         st.markdown(f"""
#         <div class="advice-card">
#             <div class="day-title">📅 {day_name}<br><small>{date_str}</small></div>
#             <div>{tip}</div>
#         </div>
#         """, unsafe_allow_html=True)
# # ----------------------------


# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from predictor import predict_energy

# # ----------------------------
# # Page Config
# # ----------------------------
# st.set_page_config(
#     page_title="AI Smart Meter Advisor",
#     page_icon="⚡",
#     layout="wide"
# )

# # ----------------------------
# # Clean Professional CSS
# # ----------------------------
# st.markdown("""
# <style>
# .stApp {
#     background-color: #F5F7FB;
#     color: #1F2937;
#     font-family: 'Inter', sans-serif;
# }

# /* Headings */
# h1, h2, h3 {
#     color: #0F172A;
#     font-weight: 700;
# }

# /* Card */
# .card {
#     background: #FFFFFF;
#     border-radius: 14px;
#     padding: 18px;
#     box-shadow: 0 6px 18px rgba(0,0,0,0.06);
#     margin-bottom: 16px;
# }

# /* Metric */
# .metric-title {
#     font-size: 14px;
#     color: #6B7280;
# }
# .metric-value {
#     font-size: 26px;
#     font-weight: 700;
#     color: #0F172A;
# }

# /* Table */
# .stDataFrame {
#     border-radius: 12px;
# }

# /* Advice Card */
# .advice-card {
#     background: #FFFFFF;
#     border-radius: 12px;
#     padding: 16px;
#     box-shadow: 0 4px 12px rgba(0,0,0,0.05);
#     border-left: 5px solid #2563EB;
#     margin-bottom: 14px;
# }

# .advice-title {
#     font-weight: 600;
#     color: #2563EB;
#     margin-bottom: 6px;
# }
# </style>
# """, unsafe_allow_html=True)

# # ----------------------------
# # Header
# # ----------------------------
# st.markdown("""
# <h1>⚡ AI Smart Meter Advisor</h1>
# <p style="color:#6B7280; font-size:16px;">
# Predict electricity consumption and receive intelligent energy-saving advice.
# </p>
# """, unsafe_allow_html=True)

# # ----------------------------
# # Load Data
# # ----------------------------
# hist_df, pred_df, avg_usage, ai_advice, forecast_explanation = predict_energy()

# # ----------------------------
# # Key Metrics
# # ----------------------------
# st.subheader("Key Insights")

# peak_days = pred_df[pred_df["Usage_Type"] == "Peak"]
# next_peak = str(peak_days.iloc[0]["Date"].date()) if not peak_days.empty else "None"
# monthly_estimate = avg_usage * 30

# col1, col2, col3 = st.columns(3)

# with col1:
#     st.markdown(f"""
#     <div class="card">
#         <div class="metric-title">Average Daily Usage</div>
#         <div class="metric-value">{avg_usage:.2f} kWh</div>
#     </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.markdown(f"""
#     <div class="card">
#         <div class="metric-title">Next Peak Day</div>
#         <div class="metric-value">{next_peak}</div>
#     </div>
#     """, unsafe_allow_html=True)

# with col3:
#     st.markdown(f"""
#     <div class="card">
#         <div class="metric-title">Estimated Monthly Usage</div>
#         <div class="metric-value">{monthly_estimate:.1f} kWh</div>
#     </div>
#     """, unsafe_allow_html=True)

# # ----------------------------
# # Prediction Chart
# # ----------------------------
# st.subheader("7-Day Electricity Usage Forecast")

# fig = px.line(
#     pred_df,
#     x="Date",
#     y="Predicted_kWh",
#     markers=True
# )

# fig.update_layout(
#     plot_bgcolor="white",
#     paper_bgcolor="white",
#     font_color="#1F2937",
#     xaxis_title="Date",
#     yaxis_title="Predicted kWh",
# )

# st.plotly_chart(fig, use_container_width=True)

# # ----------------------------
# # Forecast Summary
# # ----------------------------
# st.subheader("Forecast Summary")

# st.markdown(f"""
# <div class="card">
#     {forecast_explanation}
# </div>
# """, unsafe_allow_html=True)

# # ----------------------------
# # Historical Data
# # ----------------------------
# st.subheader("Historical Consumption")

# with st.expander("View historical daily usage"):
#     st.dataframe(
#         hist_df[["Date_only", "Daily_kWh", "Usage_Type"]],
#         use_container_width=True
#     )

# # ----------------------------
# # Prediction Table
# # ----------------------------
# st.subheader("Upcoming 7-Day Prediction")

# st.dataframe(
#     pred_df[["Date", "Predicted_kWh", "Usage_Type"]],
#     use_container_width=True
# )

# # ----------------------------
# # AI Energy Advice
# # ----------------------------
# st.subheader("AI Energy Saving Plan")

# cols = st.columns(3)

# for i, row in pred_df.iterrows():
#     date_str = row["Date"].strftime("%Y-%m-%d")
#     day_name = row["Date"].strftime("%A")
#     tip = ai_advice.get(date_str, "Use electricity efficiently today.")

#     with cols[i % 3]:
#         st.markdown(f"""
#         <div class="advice-card">
#             <div class="advice-title">{day_name} — {date_str}</div>
#             <div>{tip}</div>
#         </div>
#         """, unsafe_allow_html=True)




# import streamlit as st
# from ui import load_ui

# # Load centralized UI (CSS, styling)
# load_ui()

# # ----------------------------
# # Landing / Hero Section
# # ----------------------------
# st.markdown("""
# <div class="card" style="max-width:1000px; margin:80px auto; text-align:center;">
#     <h1>⚡ AI Smart Meter Advisor</h1>
#     <p style="font-size:18px; color:#6B7280; margin-top:10px;">
#         AI-powered electricity forecasting and energy optimization platform.
#     </p>
#     <hr style="margin:30px 0;">
#     <p style="font-size:16px; color:#4B5563;">
#         Navigate using the sidebar to access the Dashboard, Predictions, and AI Energy Saving Recommendations.
#     </p>
# </div>
# """, unsafe_allow_html=True)

# st.markdown("<br><br>", unsafe_allow_html=True)

# # Optional: quick overview cards
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.markdown("""
#     <div class="card">
#         <div class="metric-label">Predict Daily Usage</div>
#         <div class="metric-value">✓</div>
#     </div>
#     """, unsafe_allow_html=True)

# with col2:
#     st.markdown("""
#     <div class="card">
#         <div class="metric-label">Identify Peak Days</div>
#         <div class="metric-value">✓</div>
#     </div>
#     """, unsafe_allow_html=True)

# with col3:
#     st.markdown("""
#     <div class="card">
#         <div class="metric-label">AI Energy Tips</div>
#         <div class="metric-value">✓</div>
#     </div>
#     """, unsafe_allow_html=True)


import streamlit as st
from ui import load_ui

load_ui()

st.markdown("""
<div class="card" style="max-width:1000px; margin:80px auto; text-align:center; padding:40px;">
    <h1> AI SMART METER ADVISOR</h1>
    <p style="font-size:20px; color:#4b5563; line-height:1.6; margin-bottom:25px;">
        Harness the power of AI and machine learning to forecast electricity consumption, identify peak usage days, 
        and optimize energy usage for your home or business.
    </p>
    <hr style="margin:30px 0; border:1px solid #e0d7ff; width:60%;">
    <p style="font-size:18px; color:#6b7280; line-height:1.5;">
        🌟 <strong>Quick Start:</strong> Use the sidebar to explore interactive sections:
        <br>📊 <strong>Dashboard</strong>: Overview of energy usage trends.
        <br>📈 <strong>Predictions</strong>: 7-day electricity forecast.
        <br>🤖 <strong>AI Advice</strong>: AI-powered energy saving tips.
    </p>
    <p style="font-size:16px; color:#9333ea; margin-top:25px; font-weight:700;">
        Make your energy smarter, save money, and reduce your carbon footprint—all in one place!
    </p>
</div>
""", unsafe_allow_html=True)
