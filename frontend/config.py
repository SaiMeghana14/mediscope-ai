import streamlit as st

def apply_custom_styles():
    with open("frontend/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

APP_TITLE = "Mediscope-AI"
APP_SUBTITLE = "Your AI-Powered Medical Report Analyzer"

# Color themes and icons
colors = {
    "primary": "#7df9ff",
    "secondary": "#1f1f2e",
    "text": "#ffffff",
    "accent": "#00ffd5"
}

icons = {
    "Home": "🏠",
    "Results": "🧪",
    "Feedback": "🗣️",
    "History": "📜"
}

# Sidebar config
SIDEBAR_TITLE = "Navigation"
SIDEBAR_WIDTH = 300

# Page specific titles
HOME_TITLE = "🏠 Welcome to Mediscope-AI"
RESULTS_TITLE = "📄 Diagnosis Results"
FEEDBACK_TITLE = "💬 Feedback & Improvement"
HISTORY_TITLE = "📜 Diagnosis History"

# Model Info
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
PIPELINE_TASK = "text-classification"

# File Upload Config
UPLOAD_TYPES = ["pdf", "png", "jpg", "jpeg"]
MAX_FILE_SIZE_MB = 10

# Footer
FOOTER_TEXT = f"© 2025 {AUTHOR} • Made with ❤️ for better health"

# CSS path (used if you want to load dynamically)
CSS_FILE = "frontend/styles.css"



