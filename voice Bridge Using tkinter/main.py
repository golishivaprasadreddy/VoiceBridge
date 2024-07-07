import tkinter as tk
from tkinter import ttk
from threading import Thread, Event
import time
import speech_recognition as sr
from googletrans import Translator
from src.text_to_speech import text_to_speech
from src.play_audio import play_audio
import queue

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Initialize the stop event
stop_event = Event()

# Initialize the queue
msg_queue = queue.Queue()

# Function to capture audio
def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Please say something")
        audio = recognizer.listen(source)
    return audio

# Function for speech to text
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

# Function to translate text
def translate_text(text, source_lang, target_lang):
    translator = Translator()
    translated = translator.translate(text, src=source_lang, dest=target_lang)
    return translated.text

# Function to get language codes
def get_language_code(language=None):
    language_codes = {
        'English': 'en',
        'Telugu': 'te',
        'Hindi': 'hi',
        'Tamil': 'ta',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Chinese': 'zh',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Portuguese': 'pt',
        'Russian': 'ru',
        'Arabic': 'ar',
        'Bengali': 'bn',
        'Gujarati': 'gu',
        'Kannada': 'kn',
        'Malayalam': 'ml',
        'Marathi': 'mr',
        'Punjabi': 'pa',
        'Urdu': 'ur',
        'Vietnamese': 'vi',
        'Thai': 'th',
        'Italian': 'it',
        'Dutch': 'nl',
        # Add more languages and their codes as needed
    }
    if language:
        return language_codes.get(language, 'en')
    return language_codes

# Function to create GUI
def create_gui():
    global stop_event  # Ensure stop_event is accessible here

    def toggle_speaker2_fields():
        if mode_var.get() == "one_to_one":
            speaker2_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        else:
            speaker2_frame.grid_forget()

    def stop_translation():
        stop_event.set()  # Set the stop event flag to stop threads
        root.destroy()   # Close the tkinter window

    def start_translation():
        stop_event.clear()  # Clear the stop event flag
        source_language = source_lang.get()
        target_language = target_lang.get()
        source_lang_code = get_language_code(source_language)
        target_lang_code = get_language_code(target_language)

        mode = mode_var.get()
        if mode == "one_way":
            thread = Thread(target=one_way_communication_gui, args=(source_lang_code, target_lang_code))
            thread.start()
        elif mode == "one_to_one":
            source_language2 = source_lang2.get()
            target_language2 = target_lang2.get()
            source_lang_code2 = get_language_code(source_language2)
            target_lang_code2 = get_language_code(target_language2)
            thread = Thread(target=one_to_one_communication_gui, args=(source_lang_code, target_lang_code, source_lang_code2, target_lang_code2))
            thread.start()
        else:
            print("Invalid mode selected.")

    root = tk.Tk()
    root.title("Speech Translator")

    # Language selection
    language_codes = get_language_code()
    languages = list(language_codes.keys())
    source_lang = ttk.Combobox(root, values=languages)
    source_lang.set("English")
    source_lang.grid(row=0, column=0, padx=10, pady=10)

    target_lang = ttk.Combobox(root, values=languages)
    target_lang.set("English")
    target_lang.grid(row=0, column=1, padx=10, pady=10)

    # Communication mode selection
    mode_label = ttk.Label(root, text="Select communication mode:")
    mode_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    mode_var = tk.StringVar()
    mode_radio1 = ttk.Radiobutton(root, text="One-way communication", variable=mode_var, value="one_way", command=toggle_speaker2_fields)
    mode_radio1.grid(row=2, column=0, padx=10, pady=5)
    mode_radio2 = ttk.Radiobutton(root, text="One-to-one communication", variable=mode_var, value="one_to_one", command=toggle_speaker2_fields)
    mode_radio2.grid(row=2, column=1, padx=10, pady=5)

    # Language selection for Speaker 2 (one-to-one communication)
    speaker2_frame = ttk.Frame(root)

    source_lang2_label = ttk.Label(speaker2_frame, text="Source language:")
    source_lang2_label.grid(row=1, column=0, padx=5, pady=5)
    source_lang2 = ttk.Combobox(speaker2_frame, values=languages)
    source_lang2.grid(row=1, column=1, padx=5, pady=5)

    target_lang2_label = ttk.Label(speaker2_frame, text="Target language:")
    target_lang2_label.grid(row=2, column=0, padx=5, pady=5)
    target_lang2 = ttk.Combobox(speaker2_frame, values=languages)
    target_lang2.grid(row=2, column=1, padx=5, pady=5)

    # Status display area
    status_label = ttk.Label(root, text="Status:")
    status_label.grid(row=4, column=0, padx=10, pady=5)

    status_text = tk.Text(root, height=10, width=50)
    status_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    # Start and Stop buttons
    start_button = ttk.Button(root, text="Start", command=start_translation)
    start_button.grid(row=6, column=0, padx=10, pady=10)

    stop_button = ttk.Button(root, text="Stop", command=stop_translation)
    stop_button.grid(row=6, column=1, padx=10, pady=10)

    # Function to process the queue and update the GUI
    def process_queue():
        while not msg_queue.empty():
            message = msg_queue.get()
            status_text.insert(tk.END, message + "\n")
            status_text.see(tk.END)  # Scroll to the end
        root.after(100, process_queue)

    # Start processing the queue
    root.after(100, process_queue)
    root.mainloop()

# Function for one-way communication with GUI
def one_way_communication_gui(source_lang, target_lang):
    while not stop_event.is_set():
        try:
            msg_queue.put("Listening...")
            audio = capture_audio()

            msg_queue.put("Recognizing speech...")
            text = speech_to_text(audio, lang=source_lang)
            msg_queue.put(f"You said: {text}")

            if text:
                msg_queue.put("Translating...")
                translated_text = translate_text(text, source_lang, target_lang)
                msg_queue.put(f"Translated text: {translated_text}")

                msg_queue.put("Converting text to speech...")
                audio_fp = text_to_speech(translated_text, lang=target_lang)

                msg_queue.put("Playing audio...")
                play_audio(audio_fp)

                msg_queue.put("Communication completed.\n\n")
            else:
                msg_queue.put("No speech detected.\n\n")

        except Exception as e:
            msg_queue.put(f"Error occurred: {str(e)}")
            continue

        time.sleep(1)

# Function for one-to-one communication with GUI
def one_to_one_communication_gui(source_lang1, target_lang1, source_lang2, target_lang2):
    print("Starting one-to-one communication...")
    current_speaker = 1  # Start with Speaker 1
    while not stop_event.is_set():
        try:
            if current_speaker == 1:
                msg_queue.put("Speaker 1 Listening...")
                audio1 = capture_audio()

                msg_queue.put("Recognizing speech for Speaker 1...")
                text1 = speech_to_text(audio1, lang=source_lang1)
                msg_queue.put(f"Speaker 1 said: {text1}")

                if text1:
                    msg_queue.put("Translating for Speaker 2...")
                    translated_text1 = translate_text(text1, source_lang1, target_lang2)
                    msg_queue.put(f"Translated text for Speaker 2: {translated_text1}")

                    msg_queue.put("Converting translated text to speech for Speaker 2...")
                    audio_fp1 = text_to_speech(translated_text1, lang=target_lang2)

                    msg_queue.put("Playing audio for Speaker 2...")
                    play_audio(audio_fp1)

                    msg_queue.put("Speaker 1 Communication completed.\n\n")
                    current_speaker = 2

            elif current_speaker == 2:
                msg_queue.put("Speaker 2 Listening...")
                audio2 = capture_audio()

                msg_queue.put("Recognizing speech for Speaker 2...")
                text2 = speech_to_text(audio2, lang=source_lang2)
                msg_queue.put(f"Speaker 2 said: {text2}")

                if text2:
                    msg_queue.put("Translating for Speaker 1...")
                    translated_text2 = translate_text(text2, source_lang2, target_lang1)
                    msg_queue.put(f"Translated text for Speaker 1: {translated_text2}")

                    msg_queue.put("Converting translated text to speech for Speaker 1...")
                    audio_fp2 = text_to_speech(translated_text2, lang=target_lang1)

                    msg_queue.put("Playing audio for Speaker 1...")
                    play_audio(audio_fp2)

                    msg_queue.put("Speaker 2 Communication completed.\n\n")
                    current_speaker = 1

        except Exception as e:
            msg_queue.put(f"Error occurred: {str(e)}")
            continue

        time.sleep(1)

# Entry point to start the GUI
if __name__ == "__main__":
    create_gui()
