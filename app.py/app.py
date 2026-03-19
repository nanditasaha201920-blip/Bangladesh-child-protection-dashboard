import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="BD Child Protection", layout="wide")

st.title("🇧🇩 Bangladesh Child Protection Dashboard")

# --- সেফ ডেটা লোডিং ---
@st.cache_data
def load_data():
    file_path = "data/bangladesh_child_protection_data.csv"
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # ডাটা টাইপ ঠিক করা (Year যেন ইন্টিজার হয়)
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        return df.dropna(subset=['year', 'value'])
    else:
        st.error(f"❌ ফাইলটি '{file_path}' পাথে পাওয়া যায়নি!")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- ইন্টারঅ্যাক্টিভ ফিল্টার ---
    indicators = st.multiselect(
        "ইন্ডিকেটর সিলেক্ট করুন:",
        options=df["indicator"].unique(),
        default=df["indicator"].unique()[0]
    )
    
    filtered_df = df[df["indicator"].isin(indicators)]

    # --- ডাটা টেবিল ---
    with st.expander("সম্পূর্ণ ডেটা দেখুন"):
        st.dataframe(filtered_df, use_container_width=True)

    # --- লাইন চার্ট ---
    st.subheader("📈 Trends Analysis")
    fig = px.line(
        filtered_df, 
        x="year", 
        y="value", 
        color="indicator",
        markers=True,
        labels={"year": "বছর", "value": "মান", "indicator": "সূচক"},
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("দয়া করে আপনার CSV ফাইলটি 'data' ফোল্ডারে রাখুন।")

