import streamlit as st
from Home import show_home
from auth import create_users_table, add_user, validate_login
from Results import show_results
from Feedback import show_feedback
from History import show_history
from LanguageSelector import select_language
from Chatbot import show_chatbot
from database import init_db  # ✅ Import init_db

# ✅ Initialize the database
init_db()

def apply_custom_css():
    with open("frontend/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

apply_custom_css()

st.set_page_config(page_title="Mediscope-AI", layout="wide", page_icon="🧬")

create_users_table()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Sidebar Auth Panel
with st.sidebar:
    st.title("🔒 Login Panel")

    if not st.session_state.logged_in:
        tab = st.radio("Choose", ["Login", "Sign Up"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if tab == "Login":
            if st.button("Login"):
                if validate_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome, {username}!")
                else:
                    st.error("Invalid username or password.")
        else:
            if st.button("Sign Up"):
                if add_user(username, password):
                    st.success("Account created. Please login.")
                else:
                    st.warning("Username already exists.")

    else:
        st.success(f"Logged in as {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""


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

if page == "Home" or st.session_state.logged_in:
    PAGES[page]()
else:
    st.warning("🔐 Please log in to access this page.")
    
translated_title = translate_text("Mediscope AI – Your Health Assistant", target_lang)
st.title(translated_title)

mode = st.sidebar.radio("Choose mode:", ["Doctor", "Patient"])
