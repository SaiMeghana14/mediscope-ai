import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import sqlite3
import speech_recognition as sr
from transformers import pipeline
from gtts import gTTS
from fpdf import FPDF
import tempfile
import os

# -------------------------------
# Summarization pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# -------------------------------
def speak(text):
    tts = gTTS(text)
    filename = "output.mp3"
    tts.save(filename)
    st.audio(filename, format="audio/mp3")

# -------------------------------
# Mock Data
def get_mock_data():
    return pd.DataFrame({
        'Metric': ['Heart Rate', 'Blood Pressure (Systolic)', 'Blood Pressure (Diastolic)', 'SpO2', 'Temperature'],
        'Value': [82, 130, 85, 97, 98.4],
        'Normal Range': ['60-100 bpm', '90-120 mmHg', '60-80 mmHg', '95-100%', '97-99°F']
    })

# -------------------------------
# Dynamic Health Tips
def get_health_tips(symptoms):
    tips = {
        "Fever": "Stay hydrated and rest well.",
        "Cough": "Use a humidifier and avoid cold drinks.",
        "Fatigue": "Maintain a healthy diet and sleep cycle.",
        "Headache": "Reduce screen time and stay hydrated.",
        "Cold": "Drink warm fluids and avoid allergens."
    }
    return [tips.get(symptom, "Consult a doctor for personalized advice.") for symptom in symptoms]

# -------------------------------
# Recommend doctor/specialist
def recommend_doctor(df):
    if df['Severity'].max() >= 4:
        return "🔴 Critical severity detected. Please consult a General Physician or Specialist immediately."
    elif df['Severity'].max() >= 2:
        return "🟠 Moderate symptoms. Monitor closely and consult if conditions worsen."
    else:
        return "🟢 Symptoms appear mild. Home care is advised."

# -------------------------------
# Add emoji indicator based on severity
def severity_to_emoji(severity):
    if severity >= 4:
        return "🔴"
    elif severity >= 2:
        return "🟠"
    else:
        return "🟢"

# -------------------------------
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

# -------------------------------
# Save to SQLite
def save_to_database(df):
    conn = sqlite3.connect("health_data.db")
    df.to_sql("results", conn, if_exists="append", index=False)
    conn.close()

# -------------------------------
# Export to JSON
def export_json(df):
    return json.dumps(df.to_dict(orient="records"), indent=4)

# -------------------------------
# Export to CSV
def export_csv(df):
    return df.to_csv(index=False)

# -------------------------------
# Export PDF
def export_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Health Report", ln=True, align='C')
    pdf.ln()

    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Metric']}: {row['Value']} ({row['Normal Range']})", ln=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return tmp.name

# -------------------------------
# Voice Input to Text
def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, could not understand audio.")
        except sr.RequestError:
            st.error("Could not request results. Check internet.")
    return ""

# -------------------------------
# Page Logic
def show_results():
    st.title("🧾 Health Results Summary")

    df = get_mock_data()
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Line Chart of Health Metrics")
    df.plot(x='Metric', y='Value', kind='line', marker='o')
    plt.xticks(rotation=30)
    plt.ylabel("Value")
    st.pyplot()

    st.subheader("🔥 Heatmap of Health Metrics")
    df_numeric = df[['Value']].T
    sns.heatmap(df_numeric, annot=True, cmap="YlOrRd", cbar=True)
    st.pyplot()

    st.subheader("📌 Health Tips")
    selected_symptoms = st.multiselect("Select symptoms:", ["Fever", "Cough", "Fatigue", "Headache", "Cold"])
    if selected_symptoms:
        tips = get_health_tips(selected_symptoms)
        for tip in tips:
            st.info(f"💡 {tip}")

    st.subheader("🗣 Voice Narration")
    if st.button("Narrate Summary"):
        summary_text = summarizer(str(df.to_dict()))[0]['summary_text']
        st.success("Narrating Summary...")
        speak(summary_text)

    st.subheader("🎙 Voice Input (Symptoms)")
    if st.button("Start Voice Input"):
        user_text = listen_to_user()
        if user_text:
            st.write("You said:", user_text)

    st.subheader("💾 Export & Save Options")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Export JSON"):
            st.download_button("Download JSON", export_json(df), file_name="health_data.json")
    with col2:
        if st.button("Export CSV"):
            st.download_button("Download CSV", export_csv(df), file_name="health_data.csv")
    with col3:
        if st.button("Export PDF"):
            pdf_path = export_pdf(df)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="health_report.pdf")
            os.remove(pdf_path)
    with col4:
        if st.button("Save to Database"):
            save_to_database(df)
            st.success("Saved to database!")
