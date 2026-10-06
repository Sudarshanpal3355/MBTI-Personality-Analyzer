# Models.py

import os, streamlit as st, tensorflow as tf, pandas as pd

from sidebar import sidebar_header

st.set_page_config(page_title="Models", page_icon="🧩", layout="wide")


sidebar_header()


st.title("🧩 Models Overview")

MODELS_DIR = "models"

def list_models():
    rows = []
    if not os.path.isdir(MODELS_DIR):
        return pd.DataFrame(columns=["Model","File"])
    for fn in sorted(os.listdir(MODELS_DIR)):
        if fn.endswith(".keras"):
            rows.append({"Model": fn.replace(".keras",""), "File": fn})
    return pd.DataFrame(rows)

st.write("Saved models found in the `models/` directory:")

df = list_models()
st.dataframe(df, width="stretch")

st.markdown("""
**Architectures included:**
- LSTM
- BiLSTM
- TextCNN
- CNN + BiLSTM (Hybrid)
- Transformer Encoder
""")
