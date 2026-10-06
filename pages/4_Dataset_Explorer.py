# Dataset_Explorer.py

import streamlit as st, pandas as pd, plotly.express as px
from data_utils import load_dataset

from sidebar import sidebar_header

st.set_page_config(page_title="Dataset Explorer", page_icon="🗃️", layout="wide")

sidebar_header()

st.title("🗃️ Dataset Explorer")

path = st.text_input("CSV path", value="data/mbti_1.csv")

if st.button("Load Dataset"):
    try:
        df, text_col, label_col = load_dataset(path)
        st.success(f"Loaded {len(df)} rows. Text column: `{text_col}`, Label column: `{label_col}`")
        st.dataframe(df[[text_col,label_col]].head(50), width="stretch")
    except Exception as e:
        st.error(f"Failed to load: {e}")
