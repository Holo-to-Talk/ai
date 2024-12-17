import openai
from dotenv import load_dotenv
from constants import AudioToTextSettings
import os

import socketio_emit

def audio_To_Text(savedDirectory):
    load_dotenv()

    API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = API_KEY

    MODEL = AudioToTextSettings.MODEL

    audio_file_path = savedDirectory

    with open(audio_file_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe(MODEL, audio_file)

        inputContent = transcription['text']
        socketio_emit.socketio_emit_telop_add_display_none()
        socketio_emit.socketio_emit_input(inputContent)

        return inputContent