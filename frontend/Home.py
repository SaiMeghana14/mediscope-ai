import streamlit as st
from PIL import Image
from frontend.styles import apply_custom_styles

def show_home():
    apply_custom_styles()  # Apply futuristic CSS

    st.markdown("<h1 class='title'>🤖 MediScope-AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Smart Health Diagnosis & Report Generator</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("frontend/assets/ai-doctor.png", use_column_width=True)
    with col2:
        st.markdown("""
        <div class='info-box'>
        <p><strong>🧬 Enter symptoms</strong> and get a detailed possible diagnosis using AI.</p>
        <p><strong>📊 See visual charts</strong> and heatmaps based on your inputs.</p>
        <p><strong>📄 Download medical report</strong> with AI summary in PDF.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class='get-started'>
    <h3>✨ Ready to get started?</h3>
    <p>Navigate to the <strong>Results</strong> tab to enter your symptoms and generate a smart report.</p>
    </div>
    """, unsafe_allow_html=True)

if st.button("Run Test Case"):
    st.session_state["image_path"] = "frontend/assets/sample_xray.jpg"
    st.session_state["auto_test"] = True
    st.experimental_rerun()
