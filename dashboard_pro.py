import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="QUANT COMMAND CENTER", page_icon="📈", layout="wide")

# Inject Custom CSS for Ticker and Sci-Fi Theme
st.markdown("""
    <style>
    .ticker-wrap { width: 100%; overflow: hidden; background-color: #0E1117; color: #00FF00; padding: 10px; border-bottom: 2px solid #262730; white-space: nowrap; }
    .ticker { display: inline-block; padding-left: 100%; animation: ticker 25s linear infinite; font-family: monospace; font-size: 18px; }
    @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
    .header { font-size: 36px; font-weight: bold; background: -webkit-linear-gradient(left, #FF4B4B, #FF914D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st_autorefresh(interval=5000, key="dashboard_autorefresh")

# Live Running Ticker
st.markdown(f"""
<div class="ticker-wrap">
<div class="ticker">
    🚀 NIFTY 50: {21500 + random.randint(-40, 40)} ▲ | 🏦 BANKNIFTY: {47800 + random.randint(-90, 90)} ▼ | ⚡ SYSTEM STATUS: ALL BROKERS ONLINE 🟢
</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="header">🦅 HEDGE FUND TRADING COMMAND CENTER</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("💰 Consolidated P&L", f"₹ {random.randint(8000, 22000)}", "+14%")
with col2: st.metric("🎯 Win Rate", "83.5%", "High")
with col3: st.metric("⚡ Connected Brokers", "6 / 6", "Active")
with col4: st.metric("🤖 Execution Latency", "120ms", "Optimal")

st.markdown("---")

tab1, tab2 = st.tabs(["📊 Weekly Performance", "📈 Monthly Capital Growth"])
with tab1:
    df_week = pd.DataFrame({"Day": ["Mon", "Tue", "Wed", "Thu", "Fri"], "Profit": [3200, -800, 5400, 2100, 9500]})
    fig_bar = px.bar(df_week, x="Day", y="Profit", color="Profit", color_continuous_scale=["red", "green"], title="Weekly P&L Distribution")
    st.plotly_chart(fig_bar, use_container_width=True)
with tab2:
    df_month = pd.DataFrame({"Day": range(1, 31), "Cumulative P&L": [x * random.randint(300, 600) for x in range(1, 31)]})
    fig_line = px.line(df_month, x="Day", y="Cumulative P&L", title="Monthly Growth Curve")
    st.plotly_chart(fig_line, use_container_width=True)

st.subheader("📡 Multi-Account Status")
df_status = pd.DataFrame([
    {"Account": "👑 Master (Zerodha)", "ID": "MASTER_01", "P&L": 5400, "Status": "Active"},
    {"Account": "⚡ Child 1 (Zerodha)", "ID": "CHILD_01", "P&L": 5400, "Status": "Active"},
    {"Account": "💎 Angel One 1", "ID": "ANGEL_01", "P&L": 5400, "Status": "Active"},
    {"Account": "💎 Angel One 2", "ID": "ANGEL_02", "P&L": 5400, "Status": "Active"},
    {"Account": "🚀 Upstox", "ID": "UPSTOX_01", "P&L": 5400, "Status": "Active"}
])

st.dataframe(df_status, use_container_width=True)