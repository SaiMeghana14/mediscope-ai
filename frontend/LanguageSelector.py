import streamlit as st

def select_language():
    return st.selectbox("Select Language", ["en", "fr"])
