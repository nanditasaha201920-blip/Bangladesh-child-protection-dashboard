import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_local_data():
    # বর্তমান ফাইলের ডিরেক্টরি অনুযায়ী পাথ সেট করা
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "data", "bangladesh_real_data.csv")
    
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            # ডেটা ক্লিনিং (স্পেস থাকলে রিমুভ করা)
            df.columns = df.columns.str.strip()
            return df
        else:
            st.error(f"❌ ফাইলটি পাওয়া যায়নি: {file_path}")
            return pd.DataFrame() # খালি ডিএফ রিটার্ন
    except Exception as e:
        st.error(f"⚠️ ডেটা লোড করতে সমস্যা হয়েছে: {e}")
        return pd.DataFrame()

# ডেটা কল করা
df = load_local_data()

if not df.empty:
    st.success("✅ ডেটা সফলভাবে লোড হয়েছে!")
    st.write(df.head())
