import streamlit as st

def show_feedback():
    st.title("📝 Feedback")
    name = st.text_input("Your Name")
    rating = st.slider("Rate your experience", 1, 5)
    comment = st.text_area("Comments or Suggestions")

    if st.button("Submit Feedback"):
        st.success("✅ Thank you for your feedback!")
        # Store or send feedback to DB/file as needed
