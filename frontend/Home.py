mport streamlit as st
from frontend.config import API_URL

st.title("🩺 MediScope AI")
text = st.text_area("Enter medical text:")
language = st.selectbox("Choose Language", ["en", "fr"])

if st.button("Analyze"):
    with st.spinner("Processing..."):
        res = st.session_state.requests.post(
            f"{API_URL}/predict",
            headers={"x-api-key": "12345"},
            json={"text": text, "language": language}
        ).json()
        st.session_state.result = res
        st.success("Done!")
