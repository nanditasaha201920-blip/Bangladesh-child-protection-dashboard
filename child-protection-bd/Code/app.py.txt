import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import json

# --- কনফিগারেশন ---
st.set_page_config(page_title="BD Child Insights Pro", layout="wide", page_icon="🇧🇩")

# --- কাস্টম CSS (Look & Feel) ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- ডেটা লোড (সরাসরি ডিস্ট্রিক্ট ডেটা) ---
@st.cache_data
def get_district_data():
    data = {
        'district': ['Dhaka', 'CoxsBazar', 'Khulna', 'Barisal', 'Sylhet', 'Rangpur', 'Rajshahi', 'Chittagong', 'Mymensingh'],
        'poverty_rate': [25, 45, 40, 42, 35, 48, 30, 38, 41],
        'child_marriage': [15, 35, 30, 32, 25, 38, 22, 28, 31],
        'protection_risk': [40, 85, 75, 78, 65, 88, 60, 72, 76],
        'lat': [23.8103, 21.4272, 22.8456, 22.7010, 24.8949, 25.7439, 24.3745, 22.3569, 24.7471],
        'lon': [90.4125, 92.0058, 89.5403, 90.3535, 91.8687, 89.2752, 88.6042, 91.7832, 90.4036]
    }
    return pd.DataFrame(data)

df_dist = get_district_data()

# --- সাইডবার ---
st.sidebar.title("🛠️ Control Panel")
selected_metric = st.sidebar.selectbox("Select Map Metric", ["protection_risk", "poverty_rate", "child_marriage"])

# --- মেইন ড্যাশবোর্ড ---
st.title("🛡️ Strategic Child Protection Dashboard - Bangladesh")
st.markdown("### Regional Risk Analysis & Real-time Insights")

# KPI Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Highest Risk District", "Rangpur", "Critical", delta_color="inverse")
col2.metric("Avg. Protection Risk", f"{df_dist['protection_risk'].mean():.1f}%", "-2.1%")
col3.metric("Highest Poverty", f"{df_dist['poverty_rate'].max()}%", "Rangpur")
col4.metric("Avg. Child Marriage", f"{df_dist['child_marriage'].mean():.1f}%", "High")

st.divider()

# --- MAP & CHART SECTION ---
row_map_col1, row_map_col2 = st.columns([1.5, 1])

with row_map_col1:
    st.subheader(f"📍 Geospatial View: {selected_metric.replace('_', ' ').title()}")
    
    # Folium Map তৈরি
    m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles="cartodbpositron")
    
    # সার্কেল মার্কার যোগ করা (Extraordinary Visual)
    for _, row in df_dist.iterrows():
        color = 'red' if row[selected_metric] > 70 else 'orange' if row[selected_metric] > 50 else 'green'
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row[selected_metric]/5,
            popup=f"{row['district']}: {row[selected_metric]}%",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
        ).add_to(m)
    
    folium_static(m, width=700, height=500)

with row_map_col2:
    st.subheader("📊 Ranking by District")
    fig_bar = px.bar(df_dist.sort_values(selected_metric), 
                     x=selected_metric, y='district', orientation='h',
                     color=selected_metric, color_continuous_scale='Reds',
                     template="plotly_white")
    fig_bar.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

# --- নতুন ইনসাইট সেকশন ---
st.divider()
st.subheader("🔍 Automated Risk Correlation")
fig_scatter = px.scatter(df_dist, x="poverty_rate", y="protection_risk", 
                         size="child_marriage", color="district",
                         hover_name="district", text="district",
                         title="Correlation: Poverty vs Protection Risk (Size=Child Marriage)")
st.plotly_chart(fig_scatter, use_container_width=True)

# ডেটা টেবিল
with st.expander("See Raw Regional Data"):
    st.write(df_dist)
