import random
import tempfile
import os


class CeterniImage:
    def __init__(self):
        self.emotion_folders = {
            "triste": "sad",
            "feliz": "happy",
            "hola": "welcome",
        }

    def detect_emotion(self, message):
        if "triste" in message.lower():
            return "triste"
        elif "feliz" in message.lower():
            return "feliz"
        elif "hola" in message.lower():
            return "hola"
        else:
            return None

    def handle_emotion(self, emotion):
        gif_data = None
        if emotion:
            gif_data = self.send_local_emotion_gif(emotion)
        return gif_data

    def send_local_emotion_gif(self, emotion):
        if emotion in self.emotion_folders:
            emotion_folder = self.emotion_folders[emotion]
            gif_files = os.listdir(f"gifs/{emotion_folder}")
            if gif_files:
                gif_filename = random.choice(gif_files)
                gif_path = f"gifs/{emotion_folder}/{gif_filename}"
                try:
                    return gif_path
                except FileNotFoundError:
                    return None  # Cambia el mensaje de error
        return None
