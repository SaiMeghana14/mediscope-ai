from transformers import pipeline
from backend.config import NER_MODEL, SUMMARIZATION_MODEL, TRANSLATION_MODEL

def process_text(text, language):
    ner = pipeline("ner", model=NER_MODEL, grouped_entities=True)
    summary = pipeline("summarization", model=SUMMARIZATION_MODEL)
    translate = pipeline("translation_en_to_fr", model=TRANSLATION_MODEL)

    entities = ner(text)
    summary_text = summary(text, max_length=60, min_length=10, do_sample=False)[0]['summary_text']
    translation = translate(text)[0]['translation_text']

    return {
        "entities": entities,
        "summary": summary_text,
        "translation": translation
    }
