import pyaudio
import wave
import numpy as np
from dotenv import load_dotenv
from constants import VoiceRecordingSettings
import os

import socketio_emit

def voice_Recording():
    load_dotenv()

    FORMAT = pyaudio.paInt16

    CHANNELS = VoiceRecordingSettings.CHANNELS

    RATE = VoiceRecordingSettings.RATE

    CHUNK = VoiceRecordingSettings.CHUNK

    OUTPUT_FILE = VoiceRecordingSettings.OUTPUT_FILE

    THRESHOLD = VoiceRecordingSettings.THRESHOLD

    SILENCE_DURATION = VoiceRecordingSettings.SILENCE_DURATION

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format = FORMAT,
        channels = CHANNELS,
        rate = RATE,
        input = True,
        frames_per_buffer = CHUNK
    )

    socketio_emit.socketio_emit_start_telop_animation()

    frames = []
    silent_chunks = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        audio_data = np.frombuffer(data, dtype = np.int16)
        volume = np.abs(audio_data).mean()

        if volume < THRESHOLD:
            silent_chunks += 1

        else:
            silent_chunks = 0

        if silent_chunks > int(RATE / CHUNK * SILENCE_DURATION):
            socketio_emit.socketio_emit_stop_telop_animation()
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(OUTPUT_FILE, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    saved_directory = os.path.abspath(OUTPUT_FILE)

    return saved_directory