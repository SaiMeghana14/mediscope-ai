from models.model_loader import summarizer, qa_pipeline

def generate_summary(text: str, max_length=200) -> str:
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def answer_question(context: str, question: str) -> str:
    result = qa_pipeline(question=question, context=context)
    return result["answer"]
