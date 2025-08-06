import streamlit as st
import requests
from fpdf import FPDF
import base64

BACKEND = "http://localhost:8000"

def show_results():
    st.title("🩺 Diagnostic Assistant")

    # Image Upload
    st.header("1️⃣ Upload Medical Scan")
    uploaded_image = st.file_uploader("Upload an X-ray / MRI", type=["jpg", "png", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        res = requests.post(f"{BACKEND}/predict/image/", files={"file": uploaded_image})
        st.success("Prediction:")
        for r in res.json()["results"]:
            st.write(f"{r['label']} — {round(r['score']*100, 2)}%")

    # Audio Upload
    st.header("2️⃣ Upload Doctor’s Voice Note")
    uploaded_audio = st.file_uploader("Upload voice note (mp3/wav)", type=["mp3", "wav"])
    if uploaded_audio:
        st.audio(uploaded_audio)
        res = requests.post(f"{BACKEND}/predict/audio/", files={"file": uploaded_audio})
        st.success("Transcribed Note:")
        st.write(res.json()["transcription"])

    # Symptom Input
    st.header("3️⃣ Symptom Summary & Explanation")
    symptoms = st.text_area("Describe symptoms")
    if st.button("Generate Medical Summary"):
        res = requests.post(f"{BACKEND}/predict/text/", params={"symptoms": symptoms})
        st.subheader("🧠 AI Summary:")
        st.write(res.json()["summary"])
        st.subheader("🌐 Local Language (Hindi):")
        st.write(res.json()["translated"])

        # Download Report
        if st.button("Download Patient Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Symptoms:\n{symptoms}\n\nSummary:\n{res.json()['summary']}\n\nHindi:\n{res.json()['translated']}")
            pdf.output("report.pdf")
            with open("report.pdf", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="Patient_Report.pdf">📄 Download Report</a>'
                st.markdown(href, unsafe_allow_html=True)
