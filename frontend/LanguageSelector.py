import streamlit as st
from googletrans import Translator

def translate_text(text, target_lang):
    translator = Translator()
    return translator.translate(text, dest=target_lang).text

