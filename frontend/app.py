import streamlit as st
from Home import show_home
from Results import show_results
from Feedback import show_feedback
from History import show_history
from LanguageSelector import select_language

st.set_page_config(page_title="Mediscope-AI", layout="wide")

with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
PAGES = {
    "Home": show_home,
    "Language": select_language,
    "Results": show_results,
    "Feedback": show_feedback,
    "History": show_history
}

selected_page = st.sidebar.radio("Navigate", list(PAGES.keys()))
PAGES[selected_page]()

translated_title = translate_text("Mediscope AI – Your Health Assistant", target_lang)
st.title(translated_title)

mode = st.sidebar.radio("Choose mode:", ["Doctor", "Patient"])
