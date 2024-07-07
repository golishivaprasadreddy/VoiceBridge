import speech_recognition as sr

def speech_to_text(audio):
    recognizer = sr.Recognizer()
    text = recognizer.recognize_google(audio)
    return text
