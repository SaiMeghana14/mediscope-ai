import streamlit as st
import openai
from openai import OpenAIError
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import mic_recorder
from translate_module import translate_text
import uuid

# Load OpenAI API key securely
openai.api_key = st.secrets.get("openai_api_key", "")

def show_chatbot():
    st.markdown("<h2 style='color:#00f4c1;'>🧠 AI Diagnosis Assistant</h2>", unsafe_allow_html=True)
    st.markdown("💬 Ask me about any medical term, test result, or health condition from your report.")
    st.divider()

    # Get mode from session (set in app.py)
    user_mode = st.session_state.get("user_mode", "Patient")

    # System prompt depending on mode
    if user_mode == "Doctor":
        system_prompt = (
            "You are a medical assistant speaking to a doctor. "
            "Use precise medical terminology, reference relevant studies when appropriate, "
            "and assume the reader has advanced medical knowledge."
        )
    else:  # Patient mode
        system_prompt = (
            "You are a friendly medical assistant speaking to a patient. "
            "Avoid complex jargon, explain things in simple everyday language, "
            "and ensure the tone is supportive and reassuring."
        )

    # Session state for chat
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hello! I'm your AI medical assistant. Ask me anything related to your test results or medical terms."}
        ]

    # Display existing conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 🟣 Voice Input
    st.markdown("🎙️ Speak your query or type below:")
    mic_key = f"voice_{uuid.uuid4().hex}"  # unique key each render
    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="🛑 Stop",
        just_once=True,
        key=mic_key
    )

    user_input = ""

    # Transcribe voice if recorded
    if audio and "bytes" in audio:
        try:
            transcript = openai.Audio.transcribe("whisper-1", audio["bytes"])
            user_input = transcript["text"]
            st.success(f"🎧 You said: {user_input}")
        except Exception:
            st.error("Voice transcription failed.")

    # Fallback to text input
    typed_input = st.chat_input("Type your medical question here...")
    if typed_input:
        user_input = typed_input

    if user_input:
        # Detect UI language (set from app.py, default English)
        target_lang = st.session_state.get("lang_code", "en")

        # Translate user input to English for AI processing
        user_input_en = (
            translate_text(user_input, "en") if target_lang != "en" else user_input
        )

        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # AI response generation
        try:
            with st.chat_message("assistant"):
                with st.spinner("🧠 Thinking..."):
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            *[
                                {"role": m["role"], "content": m["content"]}
                                for m in st.session_state.messages
                                if m["role"] in ["user", "assistant"]
                            ]
                        ],
                        temperature=0.5,
                        max_tokens=600
                    )
                    reply_en = response.choices[0].message.content.strip()

                    # Translate back to target language if needed
                    reply_final = (
                        translate_text(reply_en, target_lang)
                        if target_lang != "en"
                        else reply_en
                    )

                    st.markdown(reply_final)

                    # 🟢 Text-to-Speech (TTS) in target language
                    try:
                        tts = gTTS(text=reply_final, lang=target_lang)
                        tts_audio = BytesIO()
                        tts.write_to_fp(tts_audio)
                        st.audio(tts_audio.getvalue(), format="audio/mp3")
                    except Exception:
                        pass  # Skip TTS errors silently

            # Save assistant message
            st.session_state.messages.append({"role": "assistant", "content": reply_final})

        except OpenAIError:
            st.error("⚠️ OpenAI API error: Please try again later.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ Sorry, I couldn't respond due to a technical error."
            })

    # Sidebar - Reset
    with st.sidebar:
        st.markdown("### 💬 Assistant Settings")
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hi again! Ask me about your medical results anytime."}
            ]
            st.success("Assistant reset!")
