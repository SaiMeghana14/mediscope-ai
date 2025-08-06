# model_utils.py
from transformers import pipeline

# Load pipelines (cached)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
ner_pipeline = pipeline("ner", grouped_entities=True, model="dslim/bert-base-NER")
summarizer_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

def answer_question(context, question):
    result = qa_pipeline(question=question, context=context)
    return result["answer"]

def extract_entities(text):
    return ner_pipeline(text)

def summarize_text(text):
    # Hugging Face summarizers have a max token limit
    chunks = [text[i:i+1024] for i in range(0, len(text), 1024)]
    summary = ""
    for chunk in chunks:
        result = summarizer_pipeline(chunk, max_length=150, min_length=40, do_sample=False)
        summary += result[0]['summary_text'] + " "
    return summary.strip()
