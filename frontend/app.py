import streamlit as st
from Home import show_home
from Results import show_results
from Feedback import show_feedback
from History import show_history
from LanguageSelector import select_language
from Chatbot import show_chatbot
from database import init_db  # ✅ Import init_db

# ✅ Initialize the database
init_db()

st.set_page_config(page_title="Mediscope-AI", layout="wide", page_icon="🧬")

# Language Selector
select_language()

with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
PAGES = {
    "Home": show_home,
    "Language": select_language,
    "Chat with AI": show_chatbot,
    "Results": show_results,
    "Feedback": show_feedback,
    "History": show_history
}

st.sidebar.title("🩺 Mediscope-AI")
selection = st.sidebar.radio("Navigate", list(PAGES.keys()))

page = PAGES[selection]
page()

translated_title = translate_text("Mediscope AI – Your Health Assistant", target_lang)
st.title(translated_title)

mode = st.sidebar.radio("Choose mode:", ["Doctor", "Patient"])
