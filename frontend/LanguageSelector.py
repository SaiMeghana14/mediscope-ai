import streamlit as st
from deep_translator import GoogleTranslator

def select_language():
    return st.selectbox("Select Language", ["en", "fr"])

def translate_text(text, target_lang='hi'):
    return GoogleTranslator(source='auto', target=target_lang).translate(text)
