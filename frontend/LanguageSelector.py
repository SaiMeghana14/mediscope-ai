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

def language_selector(default_language="English"):
    """
    Streamlit UI for selecting a language.
    Returns the selected language code (e.g., 'en', 'hi', 'te').
    """
    selected_lang_name = st.sidebar.selectbox(
        "🌐 Choose Language",
        list(SUPPORTED_LANGUAGES.keys()),
        index=list(SUPPORTED_LANGUAGES.keys()).index(default_language)
    )
    return SUPPORTED_LANGUAGES[selected_lang_name]
