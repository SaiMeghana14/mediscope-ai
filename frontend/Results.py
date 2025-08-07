import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyttsx3
from transformers import pipeline
from fpdf import FPDF
import base64
import tempfile

st.set_option('deprecation.showPyplotGlobalUse', False)

# Initialize summarizer and narrator
summarizer = pipeline("summarization")
narrator = pyttsx3.init()

# Mock health data
def get_mock_data():
    return pd.DataFrame({
        'Metric': ['Heart Rate', 'Blood Pressure (Systolic)', 'Blood Pressure (Diastolic)', 'SpO2', 'Temperature'],
        'Value': [82, 130, 85, 97, 98.4],
        'Normal Range': ['60-100 bpm', '90-120 mmHg', '60-80 mmHg', '95-100%', '97-99°F']
    })

# Dynamic health tips
def get_health_tips(symptoms):
    tips = {
        "Fever": "Stay hydrated and rest well.",
        "Cough": "Use a humidifier and avoid cold drinks.",
        "Fatigue": "Maintain a healthy diet and sleep cycle.",
        "Headache": "Reduce screen time and stay hydrated.",
        "Cold": "Drink warm fluids and avoid allergens."
    }
    return [tips.get(symptom, "Consult a doctor for personalized advice.") for symptom in symptoms]

# Recommend doctor/specialist
def recommend_doctor(df):
    if df['Severity'].max() >= 4:
        return "🔴 Critical severity detected. Please consult a General Physician or Specialist immediately."
    elif df['Severity'].max() >= 2:
        return "🟠 Moderate symptoms. Monitor closely and consult if conditions worsen."
    else:
        return "🟢 Symptoms appear mild. Home care is advised."

# Add emoji indicator based on severity
def severity_to_emoji(severity):
    if severity >= 4:
        return "🔴"
    elif severity >= 2:
        return "🟠"
    else:
        return "🟢"

# Suggested articles (demo static list)
def suggest_articles(symptoms):
    articles = {
        "Fever": "https://www.healthline.com/health/fever",
        "Cough": "https://www.webmd.com/cold-and-flu/coughs-causes-and-treatments",
        "Fatigue": "https://www.medicalnewstoday.com/articles/why-am-i-so-tired",
        "Headache": "https://www.nhs.uk/conditions/headaches/"
    }
    links = [f"- [{symptom} Guide]({articles.get(symptom, 'https://www.webmd.com/')})" for symptom in symptoms]
    return "\n".join(links)
    
# Generate PDF of results
def generate_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Health Results Summary", ln=True, align='C')

    for i in range(len(df)):
        row = df.iloc[i]
        pdf.cell(200, 10, txt=f"{row['Metric']}: {row['Value']} ({row['Normal Range']})", ln=True)

    pdf.output("/tmp/health_report.pdf")
    return "/tmp/health_report.pdf"

# Download PDF helper
def download_pdf_button(filepath):
    with open(filepath, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="health_report.pdf">📄 Download Health Report PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

# Summarize and speak results
def narrate_summary(text):
    summary = summarizer(text, max_length=60, min_length=20, do_sample=False)[0]['summary_text']
    st.subheader("📢 Summary:")
    st.info(summary)
    narrator.say(summary)
    narrator.runAndWait()

# Display Heatmap
def show_heatmap(df):
    st.subheader("📊 Health Metric Heatmap")
    df_heatmap = df[['Metric', 'Value']].set_index('Metric')
    sns.heatmap(df_heatmap, annot=True, cmap='YlOrRd', linewidths=1)
    st.pyplot()

# Main function
def show_results():
    st.title("🧪 Health Analysis Results")

    df = get_mock_data()
    st.dataframe(df, use_container_width=True)

    show_heatmap(df)

    # Narrate and summarize
    text_block = " ".join([f"{row['Metric']} is {row['Value']} which should be in {row['Normal Range']}." for _, row in df.iterrows()])
    narrate_summary(text_block)

    # Export as PDF
    st.subheader("📄 Export Report")
    pdf_path = generate_pdf(df)
    download_pdf_button(pdf_path)

    # In-app PDF preview
    with open(pdf_path, "rb") as file:
        base64_pdf = base64.b64encode(file.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500px" type="application/pdf"></iframe>'
        st.markdown("### 📑 Preview Report")
        st.markdown(pdf_display, unsafe_allow_html=True)

    # Health tips
    st.subheader("💡 Personalized Health Tips")
    selected_symptoms = st.multiselect("Select any symptoms you’re experiencing:", ["Fever", "Cough", "Fatigue", "Headache", "Cold"])
    if selected_symptoms:
        for tip in get_health_tips(selected_symptoms):
            st.success(tip)
