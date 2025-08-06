import os
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    filepath = os.path.join(destination, upload_file.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return filepath

--- models/model_loader.py ---
from transformers import pipeline
from backend.config import MODEL_NAMES

summarizer = pipeline("summarization", model=MODEL_NAMES["summarizer"])
qa_pipeline = pipeline("question-answering", model=MODEL_NAMES["qa_model"])
