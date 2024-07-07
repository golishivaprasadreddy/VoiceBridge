from gtts import gTTS
import io

def text_to_speech(text, lang='es'):
    tts = gTTS(text, lang=lang)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp