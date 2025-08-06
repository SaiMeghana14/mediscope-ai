from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .pipeline import classify_image, generate_summary, translate_to_local, transcribe_audio
from .utils import load_image, save_upload_file
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.post("/predict/image/")
async def predict_image(file: UploadFile = File(...)):
    image = load_image(file.file)
    results = classify_image(image)
    return {"results": results}

@app.post("/predict/audio/")
async def predict_audio(file: UploadFile = File(...)):
    path = f"uploads/{file.filename}"
    save_upload_file(file, path)
    transcript = transcribe_audio(path)
    return {"transcription": transcript}

@app.post("/predict/text/")
async def predict_text(symptoms: str):
    summary = generate_summary(symptoms)
    translated = translate_to_local(summary)
    return {"summary": summary, "translated": translated}
