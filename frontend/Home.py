import streamlit as st

def show_home():
    st.title("🏠 Welcome to MediScope-AI")
    st.markdown("""
        **MediScope-AI** is your AI-powered assistant for medical diagnosis support. 
        Use the sidebar to explore the tools:
        - 🖼️ Upload scans for image diagnosis
        - 🎙️ Upload doctor voice notes
        - 💬 Describe symptoms and get AI insights
    """)
