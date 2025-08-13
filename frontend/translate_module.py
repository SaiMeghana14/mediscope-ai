from deep_translator import GoogleTranslator

def translate_text(text: str, target_lang: str) -> str:
    """
    Translates given text into the target language.

    Args:
        text (str): The text to be translated.
        target_lang (str): The target language code (e.g., 'en', 'fr', 'te', 'hi').

    Returns:
        str: Translated text or None if translation fails.
    """
    if not text.strip():
        return ""
    
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        print(f"[Translation Error: {e}]")
        return None
