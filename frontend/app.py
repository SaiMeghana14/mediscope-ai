import streamlit as st
from Home import show_home
from auth import create_user_table, add_user, login_user, hash_password
from Results import show_results
from Feedback import show_feedback
from History import show_history
from LanguageSelector import select_language
from Chatbot import show_chatbot
from database import init_db  # ✅ Import init_db

# ✅ Initialize the database
init_db()
create_users_table()

def apply_custom_css():
    with open("frontend/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

apply_custom_css()

st.set_page_config(page_title="Mediscope-AI", layout="wide", page_icon="🧬")

# Sidebar Auth Panel
with st.sidebar:
    st.title("🔒 Login Panel")
menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

# Initialize session state
if choice == "Login":
    st.subheader("Login")
    username = st.text_input("User Name")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        hashed_pw = hash_password(password)
        result = login_user(username, hashed_pw)
        if result:
            st.success(f"Welcome {username}")
            # Proceed to show the app
        else:
            st.error("Invalid Username/Password")

elif choice == "Sign Up":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type='password')
    if st.button("Sign Up"):
        add_user(new_user, hash_password(new_pass))
        st.success("Account created")
        st.info("Go to Login Menu to login")

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
