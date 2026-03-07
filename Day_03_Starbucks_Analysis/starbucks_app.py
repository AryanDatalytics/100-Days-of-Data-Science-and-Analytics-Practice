import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="Starbucks Intelligence | AryanDatalytics", layout="wide")

# --- FUNCTION TO LOAD LOCAL IMAGE AS BASE64 ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# IMAGE PATH CHECK (Ensure image_7.png is in the same folder)
try:
    bin_str = get_base64('Day_04_Starbucks_Analysis/image_7.png')
except:
    bin_str = get_base64('image_7.png')

# --- ADVANCED CSS FOR OVERLAY ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117 !important; }}
    
    /* Neon Metrics */
    div[data-testid="stMetric"] {{
        background-color: #1A1C24 !important;
        border-left: 5px solid #00704A !important;
        border-radius: 10px !important;
    }}
    div[data-testid="stMetricValue"] > div {{ color: #00FF41 !important; font-size: 35px !important; }}
    div[data-testid="stMetricLabel"] > div {{ color: #D4E9E2 !important; }}

    /* Cup and Chart Container */
    .cup-container {{
        position: relative;
        width: 400px;
        height: 500px;
        margin: auto;
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }}
    .chart-overlay {{
        position: absolute;
        top: 38%; /* Adjust this to move chart up/down on the cup */
        left: 50%;
        transform: translate(-50%, -50%);
        width: 180px; /* Size of the pie chart on the cup */
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: white;'>☕ Starbucks India Market Analysis</h1>", unsafe_allow_html=True)

# --- DATA LOADING ---
df = pd.read_csv('Day_04_Starbucks_Analysis/starbucks_india_data.csv')

# --- SIDEBAR ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/d/d3/Starbucks_Corporation_Logo_2011.svg", width=100)
cities = st.sidebar.multiselect("Select Cities", options=df['City'].unique(), default=df['City'].unique())
filtered_df = df[df['City'].isin(cities)]

# --- METRICS ---
m1, m2, m3 = st.columns(3)
m1.metric("Total Stores", len(filtered_df))
m2.metric("Revenue", f"₹{filtered_df['Daily_Revenue'].sum():,.0f}")
m3.metric("Avg Order", f"₹{filtered_df['Avg_Bill_Amount'].mean():.0f}")

st.divider()

# --- MAIN SECTION: MAP & CUP OVERLAY ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📍 Outlets Distribution")
    fig_bar = px.bar(filtered_df['City'].value_counts().reset_index(), x='City', y='count', 
                     color_discrete_sequence=['#00704A'], template="plotly_dark")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("🏪 Revenue Split (On-Cup View)")
    
    # HTML for Cup and Overlay
    st.markdown('<div class="cup-container"><div class="chart-overlay">', unsafe_allow_html=True)
    
    # Pie Chart for Overlay
    fig_pie = px.pie(filtered_df, values='Daily_Revenue', names='Store_Type', 
                     color_discrete_sequence=['#00704A', '#1E3932', '#D4E9E2'], hole=0.7)
    fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0))
    fig_pie.update_traces(textinfo='none')
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; opacity: 0.5;'>AryanDatalytics | Day 04</p>", unsafe_allow_html=True)
