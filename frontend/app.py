import streamlit as st
from frontend.Home import show_home
from frontend.Results import show_results
from frontend.Feedback import show_feedback
from frontend.History import show_history

st.set_page_config(page_title="Mediscope-AI", layout="wide")

PAGES = {
    "Home": show_home,
    "Results": show_results,
    "Feedback": show_feedback,
    "History": show_history
}

choice = st.sidebar.selectbox("Navigate", list(PAGES.keys()))
PAGES[choice]()
