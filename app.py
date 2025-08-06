# app.py
import streamlit as st
from model_utils import answer_question, extract_entities, summarize_text
import os

st.set_page_config(page_title="🩺 MediScope AI", layout="wide")

st.title("🩺 MediScope AI – Your AI Medical Assistant")
st.write("A Streamlit-powered tool to analyze medical text using Hugging Face models.")

# File Upload
uploaded_file = st.file_uploader("Upload a medical text file (.txt) or PDF", type=['txt', 'pdf'])

# Read text
if uploaded_file is not None:
    file_ext = uploaded_file.name.split('.')[-1]
    if file_ext == 'txt':
        raw_text = uploaded_file.read().decode('utf-8')
    elif file_ext == 'pdf':
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            raw_text = "\n".join([page.get_text() for page in doc])
        except:
            st.error("Failed to read PDF. Please use .txt or install PyMuPDF.")
            raw_text = ""
    else:
        raw_text = ""

    st.subheader("📄 Uploaded Medical Document:")
    st.text_area("Raw Text", value=raw_text, height=250)

    # Summarization
    if st.button("🔍 Summarize"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(raw_text)
            st.success("Summary generated!")
            st.text_area("Summary", value=summary, height=200)

    # Named Entity Recognition
    if st.button("🧠 Extract Medical Entities (NER)"):
        with st.spinner("Extracting..."):
            entities = extract_entities(raw_text)
            for ent in entities:
                st.markdown(f"• **{ent['word']}** → _{ent['entity_group']}_")

    # Q&A
    question = st.text_input("Ask a medical question based on the uploaded text:")
    if question:
        with st.spinner("Thinking..."):
            answer = answer_question(raw_text, question)
            st.success(f"Answer: {answer}")
