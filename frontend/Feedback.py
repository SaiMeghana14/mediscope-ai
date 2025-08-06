import streamlit as st
from frontend.config import API_URL

st.subheader("💬 Feedback")
feedback = st.text_area("Your feedback")

if st.button("Submit Feedback"):
    st.session_state.requests.post(
        f"{API_URL}/feedback",
        json={"feedback": feedback}
    )
    st.success("Thanks for your feedback!")
