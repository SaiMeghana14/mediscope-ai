import streamlit as st
import json

st.subheader("📜 History")
try:
    with open("data/history.json") as f:
        history = json.load(f)
        for h in reversed(history[-5:]):
            st.write(f"🕓 {h['timestamp']}")
            st.code(h['input'])
            st.json(h['output'])
except:
    st.warning("No history yet.")
