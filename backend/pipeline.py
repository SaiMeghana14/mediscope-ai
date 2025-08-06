from transformers import pipeline
from .config import Config

image_classifier = pipeline("image-classification", model=Config.IMAGE_MODEL)
text_generator = pipeline("text2text-generation", model=Config.TEXT_GEN_MODEL)
translator = pipeline("translation_en_to_hi", model=Config.TRANSLATE_MODEL)
speech_to_text = pipeline("automatic-speech-recognition", model=Config.AUDIO_MODEL)

def classify_image(image):
    return image_classifier(image)

def generate_summary(symptoms):
    prompt = f"Summarize and suggest possible conditions for: {symptoms}"
    return text_generator(prompt, max_length=100, clean_up_tokenization_spaces=True)[0]['generated_text']

def translate_to_local(text):
    return translator(text)[0]['translation_text']

def transcribe_audio(audio_file):
    return speech_to_text(audio_file)['text']
