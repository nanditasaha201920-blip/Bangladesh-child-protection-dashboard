import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ১. পেজ সেটআপ
st.set_page_config(page_title="BD Child Protection", layout="wide")
st.title("🇧🇩 Bangladesh Child Protection Dashboard")

# ২. ডেটা লোড করার ফাংশন (সেফ মেথড)
@st.cache_data
def load_data():
    file_path = "data/bangladesh_child_protection_data.csv"
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # নিশ্চিত করা যে 'year' এবং 'value' কলাম সংখ্যা হিসেবে আছে
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        return df.dropna(subset=['year', 'value'])
    else:
        st.error(f"❌ ফাইলটি '{file_path}' পাথে পাওয়া যায়নি!")
        return pd.DataFrame()

df = load_data()

# ৩. যদি ডেটা সফলভাবে লোড হয়
if not df.empty:
    # --- ইন্টারঅ্যাক্টিভ ফিল্টার ---
    st.sidebar.header("ফিল্টার অপশন")
    selected_indicators = st.sidebar.multiselect(
        "ইন্ডিকেটর সিলেক্ট করুন:",
        options=df["indicator"].unique(),
        default=df["indicator"].unique()[:2] # ডিফল্ট ২টি সিলেক্ট থাকবে
    )

    # ফিল্টার করা ডেটা
    filtered_df = df[df["indicator"].isin(selected_indicators)]

    # --- মেইন কন্টেন্ট ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📄 ডেটা টেবিল")
        st.dataframe(filtered_df, use_container_width=True)

    with col2:
        st.subheader("📈 ট্রেন্ড অ্যানালাইসিস")
        fig = px.line(
            filtered_df, 
            x="year", 
            y="value", 
            color="indicator",
            markers=True,
            template="plotly_white",
            labels={"year": "বছর", "value": "মান (%)", "indicator": "সূচক"}
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("দয়া করে আপনার CSV ফাইলটি 'data' ফোল্ডারে রাখুন এবং আবার চেষ্টা করুন।")
