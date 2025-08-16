import streamlit as st 
from openai import OpenAI
from gtts import gTTS
from io import BytesIO
from streamlit_mic_recorder import mic_recorder
from translate_module import translate_text
from LanguageSelector import get_lang_code
import uuid

# Create OpenAI client using API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Test call (demo)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)   # ✅ fixed

def show_chatbot():
    st.markdown("<h2 style='color:#00f4c1;'>🧠 AI Diagnosis Assistant</h2>", unsafe_allow_html=True)
    st.markdown("💬 Ask me about any medical term, test result, or health condition from your report.")
    st.divider()

    # Detect selected language
    target_lang = get_lang_code()

    # Get mode from session state
    mode = st.session_state.get("user_mode", "Patient")
    st.info(f"📌 You are in **{mode} Mode**. Answers will be tailored accordingly.")

    # Session state for chat
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"👋 Hello! I'm your AI medical assistant in **{mode} mode**. Ask me anything related to your test results or medical terms."}
        ]

    # Display previous conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 🎙️ Voice Input
    st.markdown("🎙️ Speak your query or type below:")
    mic_key = f"voice_{uuid.uuid4().hex}"
    audio = mic_recorder(start_prompt="🎤 Start Recording", stop_prompt="🛑 Stop", just_once=True, key=mic_key)

    user_input = ""

    # Transcribe voice
    if audio and "bytes" in audio:
        try:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=BytesIO(audio["bytes"])
            )
            user_input = transcript.text
            st.success(f"🎧 You said: {user_input}")
        except Exception:
            st.error("Voice transcription failed.")

    # Fallback text input
    typed_input = st.chat_input("Type your medical question here...")
    if typed_input:
        user_input = typed_input

    if user_input:
        # Translate to English for AI
        user_input_en = translate_text(user_input, "en") if target_lang != "en" else user_input

        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            with st.chat_message("assistant"):
                with st.spinner("🧠 Thinking..."):
                    # Mode-specific instruction
                    system_prompt = (
                        "You are a highly skilled medical assistant. Provide detailed, technical explanations with medical terminology suitable for a doctor."
                        if mode == "Doctor"
                        else
                        "You are a helpful medical assistant. Provide simple, easy-to-understand explanations without heavy jargon for a patient."
                    )

                    # Get AI response in English
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
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
                    reply_en = response.choices[0].message.content.strip()   # ✅ fixed

                    # Translate response if needed
                    reply_final = translate_text(reply_en, target_lang) if target_lang != "en" else reply_en

                    st.markdown(reply_final)

                    # 🔊 Text-to-Speech
                    try:
                        tts = gTTS(text=reply_final, lang=target_lang)
                        tts_audio = BytesIO()
                        tts.write_to_fp(tts_audio)
                        st.audio(tts_audio.getvalue(), format="audio/mp3")
                    except Exception:
                        pass

            # Save reply
            st.session_state.messages.append({"role": "assistant", "content": reply_final})

        except Exception as e:
            st.error("⚠️ OpenAI API error: Please try again later.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "⚠️ Sorry, I couldn't respond due to a technical error."
            })

    # Sidebar reset button
    with st.sidebar:
        st.markdown("### 💬 Assistant Settings")
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = [
                {"role": "assistant", "content": f"Hi again! I am ready to help you in **{mode} mode**."}
            ]
            st.success("Assistant reset!")
