# frontend/Results.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import pyttsx3  # For voice narration
import base64
import os

# Optional: For AI summarization
from transformers import pipeline

# Load futuristic styles
st.markdown('<link rel="stylesheet" href="styles.css">', unsafe_allow_html=True)

# AI summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# New: Dynamic Health Tips based on symptoms
def get_health_tips(symptoms):
    tips = {
        "Fever": "Stay hydrated and rest well.",
        "Cough": "Use a humidifier and avoid cold drinks.",
        "Fatigue": "Maintain a healthy diet and sleep cycle.",
        "Headache": "Reduce screen time and stay hydrated.",
        "Cold": "Drink warm fluids and avoid allergens."
    }
    return [tips.get(symptom, "Consult a doctor for personalized advice.") for symptom in symptoms]

# New: Recommend doctor/specialist
def recommend_doctor(df):
    if df['Severity'].max() >= 4:
        return "🔴 Critical severity detected. Please consult a General Physician or Specialist immediately."
    elif df['Severity'].max() >= 2:
        return "🟠 Moderate symptoms. Monitor closely and consult if conditions worsen."
    else:
        return "🟢 Symptoms appear mild. Home care is advised."

# New: Add emoji indicator based on severity
def severity_to_emoji(severity):
    if severity >= 4:
        return "🔴"
    elif severity >= 2:
        return "🟠"
    else:
        return "🟢"

# New: Suggested articles (demo static list)
def suggest_articles(symptoms):
    articles = {
        "Fever": "https://www.healthline.com/health/fever",
        "Cough": "https://www.webmd.com/cold-and-flu/coughs-causes-and-treatments",
        "Fatigue": "https://www.medicalnewstoday.com/articles/why-am-i-so-tired",
        "Headache": "https://www.nhs.uk/conditions/headaches/"
    }
    links = [f"- [{symptom} Guide]({articles.get(symptom, 'https://www.webmd.com/')})" for symptom in symptoms]
    return "\n".join(links)

def show_results():
    st.title("🧠 Mediscope AI: Results Dashboard")

    # Sample: Use session_state or dummy data for now
    if 'results' in st.session_state:
        df = st.session_state['results']
    else:
        # Fallback demo data
        df = pd.DataFrame({
            'Symptom': ['Fever', 'Cough', 'Fatigue', 'Headache'],
            'Severity': [3, 2, 4, 1],
            'Probability (%)': [80, 65, 90, 45]
        })

    # Add emoji indicators
    df['Indicator'] = df['Severity'].apply(severity_to_emoji)

    # Display table
    st.subheader("📝 Diagnosis Results")
    st.dataframe(df, use_container_width=True)

    # AI Summary
    st.subheader("📌 AI Summary")
    summary_text = summarizer(df.to_csv(index=False), max_length=50, min_length=25, do_sample=False)[0]['summary_text']
    st.success(summary_text)

    if st.button("🔊 Narrate Summary"):
        speak(summary_text)

    st.subheader("📊 Visual Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔺 Symptom Severity Chart")
        fig, ax = plt.subplots()
        sns.barplot(x='Severity', y='Symptom', data=df, palette='coolwarm', ax=ax)
        st.pyplot(fig)

    with col2:
        st.markdown("#### 🌡️ Probability Heatmap")
        heat_df = df.pivot_table(index='Symptom', values='Probability (%)')
        fig2, ax2 = plt.subplots()
        sns.heatmap(heat_df, annot=True, cmap='YlGnBu', ax=ax2)
        st.pyplot(fig2)

    # New: Doctor recommendation section
    st.subheader("👨‍⚕️ Doctor Recommendation")
    st.info(recommend_doctor(df))

    # New: Personalized Health Tips
    st.subheader("💡 Health Tips")
    tips = get_health_tips(df['Symptom'].tolist())
    for tip in tips:
        st.write("•", tip)

    # New: Suggested Readings
    st.subheader("📚 Suggested Articles")
    st.markdown(suggest_articles(df['Symptom'].tolist()))

    # PDF Report Generator
    st.subheader("📄 Download PDF Report")

    if st.button("📥 Generate Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Mediscope AI Report", ln=True, align='C')
        pdf.ln(10)

        for index, row in df.iterrows():
            pdf.cell(200, 10, txt=f"{row['Indicator']} {row['Symptom']} - Severity: {row['Severity']}, Probability: {row['Probability (%)']}%", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt="Doctor Recommendation:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, recommend_doctor(df))

        pdf.output("report.pdf")
        with open("report.pdf", "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/pdf;base64,{base64_pdf}" download="Mediscope_Report.pdf">📤 Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
