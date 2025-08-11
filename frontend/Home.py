import streamlit as st
from PIL import Image

def show_home():
    st.markdown("""
        <div class="hero-container">
            <h1 class="title">Welcome to <span class="highlight">🤖 Mediscope-AI</span></h1>
            <p class="subtitle">Your Smart Medical Report Analyzer</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="features">
            <div class="feature-box">
                <h3>🔬 AI-Powered Analysis</h3>
                <p>Accurate and fast interpretation of your medical reports using cutting-edge AI models.</p>
            </div>
            <div class="feature-box">
                <h3>📊 Visual Insights</h3>
                <p>Interactive graphs, heatmaps, and charts to make your data understandable.</p>
            </div>
            <div class="feature-box">
                <h3>🧠 Smart Chat Assistant</h3>
                <p>Ask questions and receive AI-generated explanations and recommendations.</p>
            </div>
            <div class="feature-box">
                <h3>🌐 Multilingual Support</h3>
                <p>Select your preferred language to personalize your experience.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        .hero-container {
            text-align: center;
            padding: 3rem 1rem;
            background: linear-gradient(to right, #e0f7fa, #e8f5e9);
            border-radius: 12px;
            margin-bottom: 2rem;
        }
        .title {
            font-size: 3em;
            margin-bottom: 0.2em;
        }
        .highlight {
            color: #00796b;
        }
        .subtitle {
            font-size: 1.5em;
            color: #555;
        }
        .features {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .feature-box {
            width: 45%;
            background-color: #f9fbe7;
            margin: 1rem;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        .feature-box h3 {
            margin-top: 0;
            color: #33691e;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("frontend/assets/ai-doctor.jpg", use_column_width=True)
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

