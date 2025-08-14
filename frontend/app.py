import sys
import os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
from Home import show_home
from auth import create_user_table, add_user, login_user, hash_password
from Results import show_results
from Feedback import show_feedback
from History import show_history
from LanguageSelector import init_language_selector, get_lang_code
from translate_module import translate_text
from Chatbot import show_chatbot
from database import init_db, save_user, verify_user
from datetime import datetime, timedelta

# ---------------------------
# 1️⃣ First thing: Initialize language selector
init_language_selector(default_language="English")

# 2️⃣ Multilingual greeting
st.title("🌟 My Multilingual App")
current_lang = get_lang_code()
st.write(f"Current language code: {current_lang}")

if current_lang == "hi":
    st.write("नमस्ते! आपने हिंदी चुना है।")
elif current_lang == "te":
    st.write("హలో! మీరు తెలుగు ఎంచుకున్నారు.")
else:
    st.write("Hello! You selected English.")

# ---------------------------
# Initialize database
init_db()

# ---------------------------
# Persistent session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "login_expiry" not in st.session_state:
    st.session_state.login_expiry = None
if "user_mode" not in st.session_state:  # store doctor/patient mode
    st.session_state.user_mode = "Patient"

# ---------------------------
# Auto-logout if session expired
def check_session():
    if st.session_state.logged_in and st.session_state.login_expiry:
        if datetime.now() > st.session_state.login_expiry:
            st.warning("⚠️ Your session has expired. Please log in again.")
            logout()

# ---------------------------
# Logout
def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.login_expiry = None
    st.experimental_rerun()

# ---------------------------
# Login UI
def login_ui():
    st.title("🔐 Login to MediScope AI")
    tab1, tab2 = st.tabs(["Register", "Login"])

    # Register tab
    with tab1:
        new_user = st.text_input("Choose Username", key="reg_user")
        new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        email = st.text_input("Email", key="reg_email")
        if st.button("Register", key="reg_btn"):
            if new_user and new_pass:
                try:
                    save_user(new_user, new_pass, email)
                    st.success("✅ Account created! Please log in.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please fill in all fields.")

    # Login tab
    with tab2:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        remember_me = st.checkbox("Remember Me")

        if st.button("Login", key="login_btn"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                expiry_hours = 24 * 7 if remember_me else 1
                st.session_state.login_expiry = datetime.now() + timedelta(hours=expiry_hours)
                st.success(f"✅ Welcome back, {username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

# ---------------------------
# Main App
check_session()

if not st.session_state.logged_in:
    login_ui()
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("🚪 Log Out"):
        logout()

    st.title("🏥 MediScope AI Dashboard")

# ---------------------------
# Translate title dynamically
translated_title = translate_text("Mediscope AI – Your Health Assistant", current_lang)
st.title(translated_title)

# ---------------------------
# Load styles
with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------
# Dictionary of pages
PAGES = {
    "Home": show_home,
    "Chat with AI": show_chatbot,
    "Results": show_results,
    "Feedback": show_feedback,
    "History": show_history
}

# Sidebar navigation
st.sidebar.title("🩺 Mediscope-AI")
selection = st.sidebar.radio("Navigate", list(PAGES.keys()))
page_func = PAGES[selection]

# Login access control for pages
if selection == "Home" or st.session_state.get("logged_in", False):
    page_func()
else:
    st.warning("🔐 Please log in to access this page.")

# ---------------------------
# Mode switch
mode = st.sidebar.radio("Choose mode:", ["Doctor", "Patient"], index=0 if st.session_state.user_mode == "Doctor" else 1)
st.session_state.user_mode = mode  # Save mode persistently
