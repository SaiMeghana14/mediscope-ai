from googletrans import Translator

translator = Translator()

def translate_text(text, target_language="en"):
    """
    Translates text into the target language.
    :param text: string to translate
    :param target_language: ISO 639-1 language code (default: English 'en')
    :return: translated string
    """
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        return f"[Translation Error: {e}]"
