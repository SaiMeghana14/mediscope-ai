import streamlit as st
from database import fetch_history
def show_history():
     st.title("📜 Previous Reports")
    st.info("This section can be connected to your database or storage to fetch patient history.")
    history = fetch_history()
    for t, d, c in history:
        st.markdown(f"**🕒 {t}** — _{d}_ — Confidence: {c*100:.1f}%")
