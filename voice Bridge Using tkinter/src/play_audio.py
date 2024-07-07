import pygame
import io

def play_audio(audio_fp):
    audio_fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)