import streamlit as st
from openai import OpenAIError
import openai

# Load your OpenAI API key from secrets
openai.api_key = st.secrets.get("openai_api_key", "")

# Set up the futuristic chat UI
def show_chatbot():
    st.markdown("<h2 style='color:#00f4c1;'>🧠 AI Diagnosis Assistant</h2>", unsafe_allow_html=True)
    st.markdown("Ask me to explain any medical term, test result, or condition from your report.")
    st.divider()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello 👋 I'm your AI medical assistant. Ask me anything from your results."}
        ]

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Get user input
    if user_input := st.chat_input("Type your question here..."):
        # Append user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant reply using OpenAI
        try:
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=st.session_state.messages,
                        temperature=0.5,
                        max_tokens=500
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)

            # Append assistant message
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except OpenAIError as e:
            st.error(f"OpenAI API error: {e}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ Sorry, I couldn't respond due to a technical error."
            })

    # Option to clear chat
    with st.sidebar:
        if st.button("🔄 Reset Assistant"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi again! Ask me about your medical results anytime."}
            ]
            st.success("Assistant reset!")

