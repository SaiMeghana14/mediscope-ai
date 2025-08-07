import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyttsx3
from transformers import pipeline

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
    
# Generate health summary
def generate_summary(df):
    summary = "Here is your health report:\n"
    for _, row in df.iterrows():
        summary += f"{row['Metric']} is {row['Value']}, normal range is {row['Normal Range']}.\n"
    return summary

# Visualizations
def display_charts(df):
    st.subheader("📊 Health Metrics - Bar Chart")
    plt.figure(figsize=(8, 4))
    plt.bar(df['Metric'], df['Value'], color='skyblue')
    plt.xlabel('Metric')
    plt.ylabel('Value')
    plt.xticks(rotation=30)
    st.pyplot()

    st.subheader("🌀 Health Metrics - Pie Chart")
    plt.figure(figsize=(5, 5))
    plt.pie(df['Value'], labels=df['Metric'], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    st.pyplot()

    st.subheader("📈 Health Metrics - Line Chart")
    plt.figure(figsize=(8, 4))
    plt.plot(df['Metric'], df['Value'], marker='o')
    plt.grid(True)
    plt.ylabel("Value")
    st.pyplot()

    st.subheader("🌡️ Heatmap")
    pivot = df.pivot_table(index="Metric", values="Value")
    plt.figure(figsize=(6, 3))
    sns.heatmap(pivot, annot=True, cmap="YlGnBu", linewidths=0.5)
    st.pyplot()

# Main function
def show_results():
    st.title("🩺 Health Analysis Results")
    df = get_mock_data()

    st.subheader("📋 Health Metrics")
    st.dataframe(df, use_container_width=True)

    display_charts(df)

    st.subheader("📝 Health Summary")
    summary = generate_summary(df)
    summarized = summarizer(summary, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    st.success(summarized)

    if st.button("🔊 Narrate Summary"):
        narrator.say(summarized)
        narrator.runAndWait()

    st.subheader("💡 Suggested Health Tips")
    symptoms = st.multiselect("Select symptoms you're experiencing:", ["Fever", "Cough", "Fatigue", "Headache", "Cold"])
    if symptoms:
        tips = get_health_tips(symptoms)
        for tip in tips:
            st.info(tip)
