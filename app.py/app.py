import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="BD Child Protection", layout="wide")
st.title("🇧🇩 Bangladesh Child Protection Dashboard")

# ২. সেফ ডেটা লোডিং ফাংশন
@st.cache_data
def load_data():
    file_path = "data/bangladesh_child_protection_data.csv"
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # নিশ্চিত করা যে year এবং value সংখ্যা (Numeric) হিসেবে আছে
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        return df.dropna(subset=['year', 'value']) # খালি রো বাদ দেওয়া
    else:
        # যদি ফাইল না থাকে তবে ডামি ডেটা (টেস্ট করার জন্য)
        st.warning(f"CSV ফাইলটি '{file_path}' পাথে পাওয়া যায়নি।")
        return pd.DataFrame()

df = load_data()

# ৩. যদি ডেটা থাকে তবেই চার্ট দেখানো
if not df.empty:
    # সাইডবার ফিল্টার
    selected_indicators = st.sidebar.multiselect(
        "সিলেক্ট করুন (Indicator):",
        options=df["indicator"].unique(),
        default=df["indicator"].unique()[:2]
    )

    # ফিল্টার করা ডেটা
    filtered_df = df[df["indicator"].isin(selected_indicators)]

    # টেবিল প্রদর্শন
    st.subheader("📄 Data Overview")
    st.dataframe(filtered_df, use_container_width=True)

    # ৪. লাইন চার্ট (সঠিকভাবে কনফিগার করা)
    st.subheader("📈 Trends Over Time")
    fig = px.line(
        filtered_df, 
        x="year", 
        y="value", 
        color="indicator",
        markers=True,
        template="plotly_white",
        labels={"year": "Year", "value": "Rate (%)", "indicator": "Indicator"}
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("দয়া করে আপনার CSV ফাইলটি 'data' ফোল্ডারে রাখুন।")
