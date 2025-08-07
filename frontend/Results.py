import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyttsx3
from transformers import pipeline
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from frontend.config import APP_NAME
from frontend.styles import section_title

st.set_option('deprecation.showPyplotGlobalUse', False)

# Text summarizer and narrator
summarizer = pipeline("summarization")
narrator = pyttsx3.init()

# Sample health results data
def get_mock_data():
    return pd.DataFrame({
        'Metric': ['Heart Rate', 'Blood Pressure (Systolic)', 'Blood Pressure (Diastolic)', 'SpO2', 'Temperature'],
        'Value': [82, 130, 85, 97, 98.4],
        'Normal Range': ['60-100 bpm', '90-120 mmHg', '60-80 mmHg', '95-100%', '97-99°F']
    })

# Dynamic Health Tips based on symptoms
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

def generate_pdf(df):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 50, f"{APP_NAME} - Health Report")
    c.setFont("Helvetica", 12)
    y = height - 100
    for index, row in df.iterrows():
        line = f"{row['Metric']}: {row['Value']} (Normal: {row['Normal Range']})"
        c.drawString(50, y, line)
        y -= 25
    c.save()
    buffer.seek(0)
    return buffer

def show_results():
    st.markdown("""
        <div class="results-container">
            <h2 class="section-title">🧠 Health Analysis Results</h2>
            <p class="section-subtitle">Here’s your AI-powered diagnostic summary</p>
        </div>
    """, unsafe_allow_html=True)

    df = get_mock_data()
    st.dataframe(df, use_container_width=True, height=250)

    # 🔍 Summarize using transformer
    full_text = ". ".join([f"{row['Metric']} is {row['Value']}" for _, row in df.iterrows()])
    summary = summarizer(full_text, max_length=50, min_length=25, do_sample=False)[0]['summary_text']

    st.markdown(f"""
        <div class="summary-box">
            <h4>🧾 AI Summary:</h4>
            <p>{summary}</p>
        </div>
    """, unsafe_allow_html=True)

    # 🔊 Narrate result
    if st.button("🔊 Read Summary Aloud"):
        narrator.say(summary)
        narrator.runAndWait()

    # 📊 Charts and Heatmaps
    st.markdown("""
        <div class="charts-container">
            <h4>📈 Health Visualization</h4>
        </div>
    """, unsafe_allow_html=True)

    fig, ax = plt.subplots()
    sns.barplot(x="Metric", y="Value", data=df, palette="viridis", ax=ax)
    plt.xticks(rotation=30)
    st.pyplot(fig)

    st.markdown("""
        <div class="heatmap-box">
            <h4>🔥 Deviation Heatmap</h4>
        </div>
    """, unsafe_allow_html=True)

    heat_data = df[['Value']].T
    fig2, ax2 = plt.subplots()
    sns.heatmap(heat_data, annot=True, cmap='coolwarm', ax=ax2)
    st.pyplot(fig2)

    # 📄 Export to PDF
    if st.button("📤 Download Health Report as PDF"):
        pdf_buffer = generate_pdf(df)
        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="Health_Report.pdf",
            mime="application/pdf"
        )
