# Sidebar toggles
st.sidebar.header("🛠️ Visualization Options")
show_heatmap = st.sidebar.checkbox("Show Heatmap Overlay")
show_bar_chart = st.sidebar.checkbox("Show Prediction Confidence Chart")
show_ai_summary = st.sidebar.checkbox("Show AI Summary")

import streamlit as st
from fpdf import FPDF
import base64
import datetime
import os

# Enhanced styles for results
def set_result_style():
    st.markdown(
        """
        <style>
        .result-card {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
        }
        .result-title {
            font-size: 24px;
            font-weight: 700;
            color: #003366;
        }
        .result-text {
            font-size: 16px;
            line-height: 1.6;
            color: #333333;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Function to generate PDF report
def generate_pdf(result_text, summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, f"MEDISCOPE AI REPORT\n\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    pdf.multi_cell(0, 10, "Full Result:")
    pdf.multi_cell(0, 10, result_text)
    pdf.ln()
    pdf.multi_cell(0, 10, "AI Summary:")
    pdf.multi_cell(0, 10, summary)

    file_path = "/mnt/data/MediScope_Report.pdf"
    pdf.output(file_path)
    return file_path

def download_button(file_path, label):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="MediScope_Report.pdf">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)

def show_results():
    set_result_style()

    st.markdown("<div class='result-card'>", unsafe_allow_html=True)

    st.markdown("<h3 class='result-title'>Diagnosis Results</h3>", unsafe_allow_html=True)

    result_text = st.session_state.get("full_result", "No diagnosis result available.")
    st.markdown(f"<p class='result-text'>{result_text}</p>", unsafe_allow_html=True)

    summary = st.session_state.get("summary", "No AI summary available.")
    st.markdown("<hr>")
    st.markdown("<h4 class='result-title'>AI Summary</h4>", unsafe_allow_html=True)
    st.markdown(f"<p class='result-text'>{summary}</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 📄 Download Report")
    file_path = generate_pdf(result_text, summary)
    download_button(file_path, "⬇️ Click here to download the PDF report")

    st.success("You can now share your results or download the full report!")


# --- Enhancements: Heatmap, Graphs, AI Summary, UI ---

import seaborn as sns
import matplotlib.pyplot as plt
import openai  # Requires OPENAI_API_KEY set in .env or secrets
from io import BytesIO
import base64

# Function to generate a heatmap of results (dummy data used for illustration)
def display_heatmap(data, title="Symptom Intensity Heatmap"):
    st.markdown("### 🔥 Symptom Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(data, annot=True, fmt=".1f", cmap="YlOrRd", cbar=True, ax=ax)
    st.pyplot(fig)

# Function to display a bar chart (e.g., confidence levels for predictions)
def display_bar_chart(labels, confidences, title="Prediction Confidence Levels"):
    st.markdown("### 📊 Prediction Confidence")
    fig, ax = plt.subplots()
    ax.barh(labels, confidences, color='skyblue')
    ax.set_xlabel('Confidence (%)')
    st.pyplot(fig)

# Function to summarize results using OpenAI GPT (set your API key securely)
def generate_summary(user_input):
    openai.api_key = st.secrets.get("OPENAI_API_KEY", "")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Summarize the following medical test results:
{user_input}"}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error generating summary: {e}"

# Sample usage inside show_results (insert these in your logic where data is ready)
# Example heatmap
# import numpy as np
# sample_data = np.random.rand(5, 5)
# display_heatmap(sample_data)

# Example bar chart
# display_bar_chart(["Disease A", "Disease B"], [70, 30])

# Example AI summary
# summary_text = generate_summary("User has symptoms A, B, C with high intensity.")
# st.markdown("### 🧠 AI Summary")
# st.info(summary_text)

if mode == "Doctor":
    show_probabilities(prob_dict)
else:
    st.write(get_summary(top_class, top_prob))
