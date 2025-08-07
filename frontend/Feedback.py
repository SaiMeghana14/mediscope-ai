import streamlit as st

def show_feedback():
    st.markdown("<h2 style='color:#00f4c1;'>💬 Feedback</h2>", unsafe_allow_html=True)
    st.write("We value your feedback! Please let us know how we can improve.")

    with st.form("feedback_form"):
        name = st.text_input("Name")
        rating = st.slider("Rate your experience", 1, 5)
        comment = st.text_area("Comments or Suggestions")
        feedback = st.text_area("Your Feedback")

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("🎉 Thank you for your feedback!")
