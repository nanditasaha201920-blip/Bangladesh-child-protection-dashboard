import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -----------------------------
# CONFIG & TITLE
# -----------------------------
st.set_page_config(page_title="Bangladesh Dashboard", layout="wide", page_icon="🇧🇩")
st.title("🇧🇩 Bangladesh Child Protection & Education Dashboard")

# -----------------------------
# LOAD DATA (With Caching & Safe Path)
# -----------------------------
@st.cache_data
def load_data():
    # আপনার দেওয়া পাথটি এখানে সেট করা হয়েছে
    file_path = "child-protection-bd/Data/data/bangladesh_child_protection_data.csv"
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # ডাটা টাইপ নিশ্চিত করা
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        return df.dropna(subset=['year', 'value'])
    else:
        return None

df = load_data()

if df is None:
    st.error("❌ CSV ফাইলটি পাওয়া যায়নি। দয়া করে ফাইল পাথটি চেক করুন।")
    st.info(f"প্রত্যাশিত পাথ: child-protection-bd/Data/data/bangladesh_child_protection_data.csv")
    st.stop()

# -----------------------------
# SIDEBAR FILTERS (ইন্টারঅ্যাক্টিভিটি যোগ করা হয়েছে)
# -----------------------------
st.sidebar.header("🔍 ফিল্টার করুন")
selected_indicators = st.sidebar.multiselect(
    "ইন্ডিকেটর সিলেক্ট করুন:",
    options=df["indicator"].unique(),
    default=df["indicator"].unique()
)

filtered_df = df[df["indicator"].isin(selected_indicators)]

# -----------------------------
# KPI SECTION (Dynamic Columns)
# -----------------------------
st.subheader("📊 Key Indicators (Latest)")

# প্রতিটি ইন্ডিকেটরের সর্বশেষ ডেটা নেওয়া
latest = filtered_df.sort_values("year").groupby("indicator").last().reset_index()

if not latest.empty:
    cols = st.columns(min(len(latest), 4)) # ডায়নামিক কলাম (সর্বোচ্চ ৪টি)
    for i, row in latest.iterrows():
        cols[i % len(cols)].metric(
            label=row["indicator"].replace("_", " ").title(), 
            value=f"{row['value']}"
        )

st.divider()

# -----------------------------
# VISUALIZATIONS (Layout Optimization)
# -----------------------------
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 Trend Over Time")
    fig1 = px.line(filtered_df, x="year", y="value", color="indicator", markers=True, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("📊 Latest Comparison")
    fig2 = px.bar(latest, x="indicator", y="value", color="indicator", text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# DATA TABLE
# -----------------------------
with st.expander("📄 সম্পূর্ণ ডেটাসেট দেখুন"):
    st.dataframe(filtered_df, use_container_width=True)

