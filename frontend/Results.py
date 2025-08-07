
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

if mode == "Doctor":
    show_probabilities(prob_dict)
else:
    st.write(get_summary(top_class, top_prob))

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

