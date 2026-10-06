import streamlit as st

def sidebar_header():
    # Custom CSS for gradient sidebar title
    st.sidebar.markdown("""
    <style>
    .sidebar-title {
        font-size: 1.4rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #6EE7B7, #3B82F6, #9333EA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: -10px;
    }
    .sidebar-sub {
        font-size: 0.9rem;
        font-weight: 500;
        color: #6B7280;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # # Logo image (can replace with your own file)
    # st.sidebar.image("https://i.ibb.co/NFpMRLh/mbti-brain.png", width=120)

    # Title + subtitle
    st.sidebar.markdown("<p class='sidebar-title'>MBTI Analyzer</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p class='sidebar-sub'>AI-powered personality insights</p>", unsafe_allow_html=True)

    st.sidebar.markdown("---")
