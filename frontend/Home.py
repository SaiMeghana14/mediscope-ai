import streamlit as st

def show_home():
    st.title("🏠 Welcome to MediScope-AI")
    st.markdown("""
        **MediScope-AI** is your AI-powered assistant for medical diagnosis support. 
        Use the sidebar to explore the tools:
        - 🖼️ Upload scans for image diagnosis
        - 🎙️ Upload doctor voice notes
        - 💬 Describe symptoms and get AI insights
    """)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="padding:20px;border-radius:15px;background:#f0f2f6;">
        <h3>🧠 AI-Powered Diagnosis</h3>
        <p>Detects TB, Pneumonia, and more with accuracy.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding:20px;border-radius:15px;background:#f0f2f6;">
        <h3>📤 Upload & Analyze</h3>
        <p>Just upload your X-ray and get instant feedback.</p>
    </div>
    """, unsafe_allow_html=True)

if st.button("Run Test Case"):
    st.session_state["image_path"] = "frontend/assets/sample_xray.jpg"
    st.session_state["auto_test"] = True
    st.experimental_rerun()
