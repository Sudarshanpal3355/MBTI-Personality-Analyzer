# home.py

import streamlit as st
from sidebar import sidebar_header
import random

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# Sidebar branding
sidebar_header()

# Gradient title
st.markdown("""
<style>
.gradient-title {
    font-size: 3rem;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, #6EE7B7, #3B82F6, #9333EA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 10px;
}
.typewriter {
    font-size: 1.2rem;
    font-weight: 500;
    color: #4B5563;
    overflow: hidden;
    border-right: .15em solid #6366F1;
    white-space: nowrap;
    margin: 0 auto;
    letter-spacing: .05em;
    animation:
      typing 3.5s steps(40, end),
      blink-caret .75s step-end infinite;
}
@keyframes typing {
  from { width: 0 }
  to { width: 100% }
}
@keyframes blink-caret {
  from, to { border-color: transparent }
  50% { border-color: #6366F1; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='gradient-title'>🧠 MBTI Personality Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p class='typewriter'>Discover your personality type, emotions, and sentiment from text ✨</p>", unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("🔍 What this app does")
    st.markdown("""
    - Predicts **MBTI personality type** from your writing.  
    - Visualizes results with **gauges, tables, and charts**.  
    - Detects **emotions** (joy, sadness, anger, fear, trust, disgust, surprise, anticipation).  
    - Shows **sentiment balance** (positive, negative, neutral).  
    - Compares performance of multiple ML models.  
    """)

    st.success("💡 Tip: Try pasting a paragraph about yourself in the Analyzer page!")

# with col2:
#     st.image("https://i.ibb.co/NFpMRLh/mbti-brain.png", caption="AI-powered Personality Insights", use_column_width=True)

with col2:
    st.markdown("""
    <div style="padding:20px; border-radius:10px; background:linear-gradient(90deg, #4e54c8, #8f94fb); color:white; text-align:center;">
        <h2>🔮 Personality Analyzer</h2>
        <p>Get insights into your MBTI type with cutting-edge AI models.</p>
    </div>
    """, unsafe_allow_html=True)




# st.markdown("---")
# st.caption("Developed with ❤️ by **Sudarshan Pal** & **Basundhara Jadav**")


st.markdown("---", unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align: center;
    font-style: italic;
    color: #90908d;
    padding: 10px;
    font-size: 15px;
">
    ⚠️ Developed with ❤️
</div>
""", unsafe_allow_html=True)
