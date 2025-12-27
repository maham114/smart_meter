import streamlit as st

def load_ui():
    st.set_page_config(
        page_title="⚡ AI Smart Meter Advisor",
        page_icon="⚡",
        layout="wide"
    )

    st.markdown("""
    <style>
    /* ---------------- App Background ---------------- */
    .stApp {
        background: linear-gradient(135deg, #fafafa, #fbeaff); /* soft lavender-pink */
        font-family:'Inter', sans-serif;
        color:#1f2937;
    }

    /* ---------------- Sidebar ---------------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,#e0bbff,#fbcfe8);
        color:#1f2937;
        font-weight:900;
        font-size:18px;
        padding-top:30px;
    }
    [data-testid="stSidebar"] h2 {
        color:#7c3aed;
        font-size:28px;
        font-weight:900;
        text-align:center;
        margin-bottom:20px;
    }
    [data-testid="stSidebar"] div {
        padding:10px 5px;
        font-weight:700;
        font-size:18px;
        color:#1f2937;
    }

    /* ---------------- Headings ---------------- */
    h1 { font-size:50px; font-weight:900; color:#7c3aed; margin-bottom:20px; text-align:center; }
    h2 { font-size:36px; font-weight:800; color:#9333ea; margin-bottom:15px; }
    h3 { font-size:28px; font-weight:700; color:#1f2937; }

    /* ---------------- Cards ---------------- */
    .card {
        background: linear-gradient(145deg,#ffffff,#f3e8ff);
        border-radius:22px;
        padding:28px;
        box-shadow:0 14px 40px rgba(0,0,0,0.08);
        margin-bottom:25px;
        transition:0.3s ease;
    }
    .card:hover { box-shadow:0 20px 60px rgba(0,0,0,0.15); transform:translateY(-3px); }

    /* ---------------- Metrics ---------------- */
    .metric-label { font-size:14px; color:#6B7280; text-transform:uppercase; letter-spacing:0.5px; }
    .metric-value { font-size:36px; font-weight:800; margin-top:6px; }
    .metric-primary { color:#7c3aed; }
    .metric-success { color:#10b981; }
    .metric-warning { color:#f59e0b; }
    .metric-accent { color:#9333ea; }

    /* ---------------- Advice Cards ---------------- */
    .advice-card { border-radius:20px; padding:24px; box-shadow:0 14px 40px rgba(0,0,0,0.08); margin-bottom:22px; transition:0.3s ease; }
    .advice-indigo { background:#ede9fe; border-left:6px solid #7c3aed; }
    .advice-pink { background:#fdf2f8; border-left:6px solid #db2777; }
    .advice-teal { background:#ecfeff; border-left:6px solid #06b6d4; }
    .advice-orange { background:#fff7ed; border-left:6px solid #f97316; }
    .advice-card:hover { transform:translateY(-3px); box-shadow:0 20px 50px rgba(0,0,0,0.15); }
    .advice-title { font-weight:700; margin-bottom:8px; font-size:16px; color:#1f2937; }

    /* ---------------- Tables ---------------- */
    .stDataFrame { background-color:#fffafa !important; border-radius:14px; padding:10px; }
    .stDataFrame th { background: linear-gradient(90deg,#7c3aed,#fbb6ce) !important; color:white !important; }

    /* ---------------- Plotly ---------------- */
    .plotly-graph-div { background-color:#ffffff !important; border-radius:22px; padding:12px; }
    </style>
    """, unsafe_allow_html=True)
