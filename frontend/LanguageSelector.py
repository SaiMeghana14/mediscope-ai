# LanguageSelector.py
import streamlit as st

# List of supported languages
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Urdu": "ur",
}

def init_language_selector(default_language="English"):
    """
    Creates the language selector in the sidebar if it hasn't been set.
    Stores the selected language code in st.session_state['language'].
    """
    if "language" not in st.session_state:
        st.session_state.language = SUPPORTED_LANGUAGES[default_language]

    selected_lang_name = st.sidebar.selectbox(
        "🌐 Choose Language",
        list(SUPPORTED_LANGUAGES.keys()),
        index=list(SUPPORTED_LANGUAGES.keys()).index(
            default_language if "language" not in st.session_state 
            else get_lang_name(st.session_state.language)
        ),
        key="sidebar_language_selector"
    )
    st.session_state.language = SUPPORTED_LANGUAGES[selected_lang_name]

def get_lang_code():
    """Returns current selected language code."""
    return st.session_state.get("language", "en")

def get_lang_name(lang_code):
    """Returns language name from code."""
    for name, code in SUPPORTED_LANGUAGES.items():
        if code == lang_code:
            return name
    return "English"
