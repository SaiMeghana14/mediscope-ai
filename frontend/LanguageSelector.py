# LanguageSelector.py
import streamlit as st

try:
    from googletrans import Translator
    translator = Translator()
    translation_enabled = True
except ImportError:
    translation_enabled = False
    translator = None

def translate_text(text, dest_lang="en"):
    """Translate text to the given language, fallback to original text."""
    if translation_enabled and translator:
        try:
            result = translator.translate(text, dest=dest_lang)
            return result.text
        except Exception as e:
            st.warning(f"Translation failed, showing English. Error: {e}")
            return text
    else:
        return text

def language_selector():
    """Streamlit language selection dropdown."""
    st.sidebar.subheader("🌐 Select Language")
    languages = {
        "English": "en",
        "Hindi": "hi",
        "Telugu": "te",
        "Tamil": "ta",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Bengali": "bn",
        "Gujarati": "gu",
        "Marathi": "mr",
        "Urdu": "ur"
    }
    selected_language = st.sidebar.selectbox("Language", list(languages.keys()))
    return languages[selected_language]

if __name__ == "__main__":
    # Example usage
    st.title("Language Selector Test")
    lang_code = language_selector()
    st.write(translate_text("Hello, welcome to the AI Doctor!", lang_code))
