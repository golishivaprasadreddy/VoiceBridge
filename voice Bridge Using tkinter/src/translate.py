from googletrans import Translator

def translate_text(text, dest_lang='es'):
    translator = Translator()
    translated = translator.translate(text, dest=dest_lang)
    return translated.text