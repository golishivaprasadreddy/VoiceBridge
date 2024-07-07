import speech_recognition as sr

def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Please say something")
        audio = recognizer.listen(source, timeout=100, phrase_time_limit=10)
    return audio