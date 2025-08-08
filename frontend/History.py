import streamlit as st

def show_history():
    st.markdown("<h2 style='color:#00f4c1;'>📜 Chat History</h2>", unsafe_allow_html=True)

    if "messages" in st.session_state and len(st.session_state.messages) > 1:
        for i, msg in enumerate(st.session_state.messages):
            with st.expander(f"{msg['role'].capitalize()} Message #{i+1}"):
                st.markdown(msg["content"])
    else:
        st.info("No chat history yet. Ask something in the chatbot to start.")

    # This part should be **outside** the else block
    st.title("📜 Previous Reports")
    st.info("This section can be connected to your database or storage to fetch patient history.")
    
    # If you haven't defined fetch_history yet, you’ll get an error.
    # Add a mock or import before using it
    try:
        history = fetch_history()
        for t, d, c in history:
            st.markdown(f"**🕒 {t}** — _{d}_ — Confidence: {c*100:.1f}%")
    except NameError:
        st.warning("⚠️ fetch_history() is not defined. Please implement it or import from the backend.")
