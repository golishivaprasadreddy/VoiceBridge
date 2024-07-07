import speech_recognition as sr
from src.translate import translate_text
from src.text_to_speech import text_to_speech
from src.play_audio import play_audio

import time
import msvcrt  # Import the msvcrt module

def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Please say something")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
    return audio

def speech_to_text(audio, lang='en-US'):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio, language=lang)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    return ""

def get_language_code(language=None):
    language_codes ={
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Amharic': 'am',
    'Arabic': 'ar',
    'Armenian': 'hy',
    'Azerbaijani': 'az',
    'Basque': 'eu',
    'Belarusian': 'be',
    'Bengali': 'bn',
    'Bosnian': 'bs',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Cebuano': 'ceb',
    'Chichewa': 'ny',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Corsican': 'co',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Esperanto': 'eo',
    'Estonian': 'et',
    'Filipino': 'tl',
    'Finnish': 'fi',
    'French': 'fr',
    'Frisian': 'fy',
    'Galician': 'gl',
    'Georgian': 'ka',
    'German': 'de',
    'Greek': 'el',
    'Gujarati': 'gu',
    'Haitian Creole': 'ht',
    'Hausa': 'ha',
    'Hawaiian': 'haw',
    'Hebrew': 'iw',
    'Hindi': 'hi',
    'Hmong': 'hmn',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Igbo': 'ig',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Javanese': 'jw',
    'Kannada': 'kn',
    'Kazakh': 'kk',
    'Khmer': 'km',
    'Kinyarwanda': 'rw',
    'Korean': 'ko',
    'Kurdish (Kurmanji)': 'ku',
    'Kyrgyz': 'ky',
    'Lao': 'lo',
    'Latin': 'la',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Luxembourgish': 'lb',
    'Macedonian': 'mk',
    'Malagasy': 'mg',
    'Malay': 'ms',
    'Malayalam': 'ml',
    'Maltese': 'mt',
    'Maori': 'mi',
    'Marathi': 'mr',
    'Mongolian': 'mn',
    'Myanmar (Burmese)': 'my',
    'Nepali': 'ne',
    'Norwegian': 'no',
    'Odia (Oriya)': 'or',
    'Pashto': 'ps',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Punjabi': 'pa',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Samoan': 'sm',
    'Scots Gaelic': 'gd',
    'Serbian': 'sr',
    'Sesotho': 'st',
    'Shona': 'sn',
    'Sindhi': 'sd',
    'Sinhala': 'si',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Somali': 'so',
    'Spanish': 'es',
    'Sundanese': 'su',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tajik': 'tg',
    'Tamil': 'ta',
    'Tatar': 'tt',
    'Telugu': 'te',
    'Thai': 'th',
    'Turkish': 'tr',
    'Turkmen': 'tk',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Uyghur': 'ug',
    'Uzbek': 'uz',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Xhosa': 'xh',
    'Yiddish': 'yi',
    'Yoruba': 'yo',
    'Zulu': 'zu'
}
    if language:
        return language_codes.get(language, 'en')
    return language_codes

def one_way_communication(source_lang, target_lang):
    print("Press 'e' to exit the program.")
    while True:
        try:
            if msvcrt.kbhit() and msvcrt.getch() == b'e':
                print("Exiting program.")
                break

            print("Listening...")
            audio = capture_audio()

            print("Recognizing speech...")
            text = speech_to_text(audio, lang=source_lang)
            print(f"You said: {text}")

            print("Translating...")
            translated_text = translate_text(text, dest_lang=target_lang)
            print(f"Translated text: {translated_text}")

            print("Converting text to speech...")
            audio_fp = text_to_speech(translated_text, lang=target_lang)

            print("Playing audio...")
            play_audio(audio_fp)

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            continue

        time.sleep(1)

def one_to_one_communication(source_lang1, target_lang1, source_lang2, target_lang2):
    print("Press 'e' to exit the program.")
    while True:
        try:
            if msvcrt.kbhit() and msvcrt.getch() == b'e':
                print("Exiting program.")
                break

            for speaker in [1, 2]:
                if speaker == 1:
                    print(f"Speaker 1 ({source_lang1}), Listening...")
                    source_lang = source_lang1
                    target_lang = target_lang1
                else:
                    print(f"Speaker 2 ({source_lang2}), Listening...")
                    source_lang = source_lang2
                    target_lang = target_lang2
                    
                audio = capture_audio()

                print(f"Recognizing speech from Speaker {speaker}...")
                text = speech_to_text(audio, lang=source_lang)
                print(f"Speaker {speaker} said: {text}")

                print(f"Translating from {source_lang} to {target_lang}...")
                translated_text = translate_text(text, dest_lang=target_lang)
                print(f"Translated text: {translated_text}")

                print("Converting translated text to speech...")
                audio_fp = text_to_speech(translated_text, lang=target_lang)

                print("Playing audio...")
                play_audio(audio_fp)

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            continue

        time.sleep(1)

def main():
    print("Select communication mode:")
    print("1. One-way communication")
    print("2. One-to-one communication")
    mode = input("Enter 1 or 2: ").strip()

    language_codes = get_language_code()
    print("Available languages:")
    for language in language_codes.keys():
        print(language)

    print("Select the source language:")
    source_language = input("Source language: ").strip()
    source_lang_code = get_language_code(source_language)

    print("Select the target language:")
    target_language = input("Target language: ").strip()
    target_lang_code = get_language_code(target_language)

    if mode == '1':
        one_way_communication(source_lang_code, target_lang_code)
    elif mode == '2':
        print("Select the source language for Speaker 2:")
        source_language2 = input("Source language for Speaker 2: ").strip()
        source_lang_code2 = get_language_code(source_language2)

        print("Select the target language for Speaker 2:")
        target_language2 = input("Target language for Speaker 2: ").strip()
        target_lang_code2 = get_language_code(target_language2)

        one_to_one_communication(source_lang_code, target_lang_code, source_lang_code2, target_lang_code2)
    else:
        print("Invalid selection. Exiting program.")

if __name__ == "__main__":
    main()