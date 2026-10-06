import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

# Title
st.title("ℹ️ About the MBTI Personality Analyzer")

# Overview
st.markdown("""
This project demonstrates a **hybrid deep learning approach** for predicting **MBTI personality types** 
from free text using **TensorFlow** and **NLP techniques**.  
It integrates multiple deep learning architectures with ensemble predictions to improve accuracy, 
while also giving **emotion insights** and **sentiment balance** for a more holistic analysis.
""")

# Key Features
st.subheader("✨ Key Features")
st.markdown("""
- **MBTI Prediction** → Classifies across 4 dichotomies *(E/I, S/N, T/F, J/P)*.  
- **Ensemble Models** → LSTM, BiLSTM, CNN, CNN-BiLSTM, Transformer combined for robust predictions.  
- **Interactive UI** → Live gauges, radar charts, bar plots, sentiment pie chart, and per-model scores.  
- **Emotion Analyzer** → Lexicon-based scoring for 8 Plutchik emotions (joy, sadness, anger, fear, trust, disgust, surprise, anticipation).  
- **Validation Reports** → Displays per-dichotomy accuracy, confusion matrices, and model comparison.  
- **Demo Ready** → Preloaded text samples and downloadable examples.
""")

# Technologies Used
st.subheader("🛠 Technologies Used")
st.markdown("""
- **Frontend/UI** → Streamlit, Plotly  
- **Backend/ML** → TensorFlow / Keras, Scikit-learn, NLTK  
- **Data Handling** → Pandas, NumPy  
- **Visualization** → Gauges, radar charts, bar plots, pie charts  
- **Deployment** → Streamlit Cloud / Render
""")

# Limitations
st.subheader("⚠️ Limitations")
st.markdown("""
- The **emotion component** is a simple lexicon + sentiment model (not clinically validated).  
- MBTI itself is a **popular framework**, but not a definitive psychological diagnostic tool.  
- Model accuracy depends heavily on **dataset quality** and **training size**.  
""")

# Future Improvements
st.subheader("🚀 Future Improvements")
st.markdown("""
- Expand dataset for better generalization.  
- Integrate **transformer-based embeddings** (BERT, RoBERTa).  
- Add **user history dashboard** with trend graphs.  
- Deploy as a **mobile/web app** with API support.  
""")

# Footer / Credits
st.markdown("---")
st.caption("⚠️ *Disclaimer: This tool is for educational and research purposes only, not for clinical or psychological evaluation.*")
st.markdown(
    "<div style='text-align: center; padding: 10px;'>"
    "Developed with ❤️"
    "</div>",
    unsafe_allow_html=True
)