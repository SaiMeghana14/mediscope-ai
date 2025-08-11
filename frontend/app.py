import streamlit as st
from Home import show_home
from auth import create_user_table, add_user, login_user, hash_password
from Results import show_results
from Feedback import show_feedback
from History import show_history
from LanguageSelector import select_language
from Chatbot import show_chatbot
from database import init_db, save_user, verify_user
from datetime import datetime, timedelta

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

       # ---------------- REGISTER ----------------
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

    # ---------------- LOGIN ----------------
    with tab2:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        remember_me = st.checkbox("Remember Me")

        if st.button("Login", key="login_btn"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username

                # If Remember Me checked → 7-day expiry, else 1-hour session
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

    # Import after login to prevent early execution
    from Results import show_results
    from History import show_history
    from Chatbot import show_chatbot

    menu = st.sidebar.radio("Navigation", ["Chatbot", "Results", "History"])
    if menu == "Chatbot":
        show_chatbot()
    elif menu == "Results":
        show_results()
    elif menu == "History":
        show_history()


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
