import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    IMAGE_MODEL = "microsoft/resnet-50"
    TEXT_GEN_MODEL = "google/flan-t5-base"
    TRANSLATE_MODEL = "Helsinki-NLP/opus-mt-en-hi"  # English to Hindi
    AUDIO_MODEL = "openai/whisper-base"
