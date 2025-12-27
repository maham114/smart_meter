import streamlit as st
from ui import load_ui
from predictor import predict_energy_cached
import plotly.express as px

load_ui()
hist_df, pred_df, avg_usage, ai_advice, forecast_explanation = predict_energy_cached()

st.markdown("<h1>📊 Energy Dashboard</h1>", unsafe_allow_html=True)

# Metrics
peak_days = pred_df[pred_df["Usage_Type"]=="Peak"]
next_peak = str(peak_days.iloc[0]['Date'].date()) if not peak_days.empty else "No Peak"
monthly_estimate = avg_usage*30

cols = st.columns(3)
metrics = [
    ("Avg Daily Usage", f"{avg_usage:.2f} kWh", "metric-success"),
    ("Next Peak Day", next_peak, "metric-warning"),
    ("Estimated Monthly Usage", f"{monthly_estimate:.1f} kWh", "metric-accent")
]

for col, (label,value,color) in zip(cols, metrics):
    col.markdown(f"""
    <div class="card" style="text-align:center;">
        <div class="metric-label">{label}</div>
        <div class="metric-value {color}">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# Forecast Chart
st.subheader("📈 7-Day Usage Forecast")
fig = px.line(pred_df, x="Date", y="Predicted_kWh", markers=True)
fig.update_traces(line_color="#7c3aed", fill='tozeroy', fillcolor='rgba(124,58,237,0.15)')
fig.update_layout(plot_bgcolor="#fbeaff", paper_bgcolor="#fbeaff", font_color="#1f2937", title_x=0.5)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Forecast Summary
st.subheader("📝 Forecast Summary")
st.markdown(f"""
<div class="card" style="background:linear-gradient(135deg,#ede9fe,#f3e8ff); padding:25px;">
{forecast_explanation}
</div>
""", unsafe_allow_html=True)
