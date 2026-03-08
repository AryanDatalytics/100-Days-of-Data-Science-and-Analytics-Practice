import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="SBUX Precision BI | 2026", layout="wide", page_icon="☕")

# --- 2. DATA LOADING ---
@st.cache_data
def load_ytd_data():
    cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Gurgaon', 'Kolkata']
    weights = [0.28, 0.24, 0.20, 0.10, 0.06, 0.05, 0.04, 0.03]
    channels = ['Mall', 'High Street', 'Airport', 'Drive-Thru']
    ch_weights = [0.45, 0.34, 0.20, 0.01]
    
    return pd.DataFrame({
        'City': np.random.choice(cities, 480, p=weights),
        'Store_Type': np.random.choice(channels, 480, p=ch_weights),
        'Daily_Revenue': np.random.randint(65000, 82000, 480),
        'Avg_Ticket': np.random.randint(310, 345, 480)
    })

df = load_ytd_data()

# --- 3. MASTER CSS (REFINED SPACING & UX) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Dancing+Script:wght@700&display=swap');
    .stApp { background-color: #0E1117 !important; font-family: 'Inter', sans-serif !important; }
    
    .hanging-board {
        background-color: #161B22; border: 2px solid #3d2b1f; border-radius: 15px;
        padding: 15px; text-align: center; margin-bottom: 25px; position: relative;
    }
    .kpi-card {
        background: #1A1C24; border-left: 4px solid #00704A; border-radius: 8px;
        padding: 12px; transition: 0.3s;
    }
    .kpi-card:hover { border-left: 4px solid #00FF41; background: #22252E; transform: translateY(-2px); }
    .kpi-val { color: #00FF41; font-size: 26px; font-weight: 700; margin: 0; }
    .kpi-label { color: #8B949E; font-size: 11px; text-transform: uppercase; margin: 0; }
    
    /* Precision Table Styling */
    .precision-box {
        background: #111418; border: 1px solid #30363D; border-radius: 8px;
        padding: 10px; margin-top: 10px; font-size: 13px; color: #D4E9E2;
        display: flex; justify-content: space-around;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (UX ENHANCEMENTS) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/d/d3/Starbucks_Corporation_Logo_2011.svg", width=70)
st.sidebar.subheader("📅 Reporting & Comparison")

# Comparison Toggle (UX Suggestion)
compare_mode = st.sidebar.toggle("Enable Period Comparison (YoY/MoM)")
if compare_mode:
    st.sidebar.caption("📊 Comparing Q1 2026 vs Q1 2025")

st.sidebar.divider()

# Filter Reset Logic (Quick Win)
if st.sidebar.button("🔄 Reset All Filters"):
    st.session_state['cities'] = list(df['City'].unique())
    st.rerun()

selected_cities = st.sidebar.multiselect(
    "Select Geography", 
    options=df['City'].unique(), 
    default=df['City'].unique(),
    key='cities'
)
filtered_df = df[df['City'].isin(selected_cities)]

# --- 5. HEADER ---
st.markdown("""
    <div class="hanging-board">
        <div style="font-family:'Dancing Script'; color:white; font-size:40px;">Starbucks Precision Intel</div>
        <div style="color:#00704A; letter-spacing:2px; font-weight:700; font-size:12px;">YTD PERFORMANCE CONSOLE | MARCH 2026</div>
    </div>
""", unsafe_allow_html=True)

# --- 6. KPIs (WITH TREND INDICATORS) ---
k1, k2, k3, k4 = st.columns(4)
ann_rev_cr = (filtered_df['Daily_Revenue'].sum() * 365) / 10000000

with k1:
    st.markdown(f'<div class="kpi-card"><p class="kpi-label">Outlets</p><p class="kpi-val">{len(filtered_df)} <span style="font-size:12px; color:#00FF41;">↑ 4%</span></p></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card"><p class="kpi-label">Revenue (Est.)</p><p class="kpi-val">₹{ann_rev_cr:,.0f}Cr <span style="font-size:12px; color:#00FF41;">↑ 8%</span></p></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card"><p class="kpi-label">Ticket Size</p><p class="kpi-val">₹{filtered_df["Avg_Ticket"].mean():.0f} <span style="font-size:12px; color:#FF4B4B;">↓ 1%</span></p></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-card"><p class="kpi-label">Market Share</p><p class="kpi-val">74% <span style="font-size:12px; color:#00FF41;">↑ 2.1%</span></p></div>', unsafe_allow_html=True)

# --- 7. CHARTS SECTION ---
c_left, c_right = st.columns([1.3, 1])

with c_left:
    st.subheader("📍 City-wise Concentration")
    city_counts = filtered_df['City'].value_counts().reset_index()
    fig_bar = px.bar(city_counts, x='City', y='count', 
                     hover_data={'count': True}, # Tooltip Win
                     color='count', color_continuous_scale='Greens', template="plotly_dark")
    fig_bar.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          height=350, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_bar, use_container_width=True)

with c_right:
    st.subheader("🏪 Revenue Split (Format)")
    pie_data = filtered_df.groupby('Store_Type')['Daily_Revenue'].sum().reset_index()
    # Calculating values for Precision Table
    pie_data['Cr'] = (pie_data['Daily_Revenue'] * 365) / 10000000
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=pie_data['Store_Type'], values=pie_data['Daily_Revenue'], hole=0.7,
        textinfo='percent', marker=dict(colors=['#1E3932', '#00704A', '#217346', '#D4E9E2'])
    )])
    fig_pie.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"), 
                          paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=300)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 8. PRECISION BREAKDOWN TABLE (Quick Win) ---
st.markdown("### 📊 Precision Financial Breakdown")
format_stats = " | ".join([f"**{row['Store_Type']}**: ₹{row['Cr']:,.0f}Cr" for _, row in pie_data.iterrows()])
st.markdown(f'<div class="precision-box">{format_stats}</div>', unsafe_allow_html=True)

# --- 9. DRILLDOWN ---
with st.expander("🔍 Operational Store Logs"):
    st.dataframe(filtered_df.head(20), use_container_width=True)

st.markdown("<p style='text-align:center; color:#444; font-size:10px; margin-top:40px;'>AryanDatalytics | BI Precision Console v3.0</p>", unsafe_allow_html=True)
