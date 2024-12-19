import pyaudio
import wave
import numpy as np
from dotenv import load_dotenv
from constants import VoiceRecordingSettings
import os

import socketio_emit

# ボイス録音
def voice_Recording():
    # .env
    load_dotenv()

    # フォーマット指定
    FORMAT = pyaudio.paInt16

    # チャンネル取得
    CHANNELS = VoiceRecordingSettings.CHANNELS

    # レート取得
    RATE = VoiceRecordingSettings.RATE

    # チャンク取得
    CHUNK = VoiceRecordingSettings.CHUNK

    # 出力ファイル取得
    OUTPUT_FILE = VoiceRecordingSettings.OUTPUT_FILE

    # 無音判定の閾値取得
    THRESHOLD = VoiceRecordingSettings.THRESHOLD

    # 録音終了秒数取得
    SILENCE_DURATION = VoiceRecordingSettings.SILENCE_DURATION

    audio = pyaudio.PyAudio()

    stream = audio.open(
        # フォーマット
        format = FORMAT,
        # チャンネル
        channels = CHANNELS,
        # レート
        rate = RATE,
        # 入力
        input = True,
        # チャンク
        frames_per_buffer = CHUNK
    )

    # Animationスタート
    socketio_emit.socketio_emit_start_telop_animation()

    frames = []
    silent_chunks = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        audio_data = np.frombuffer(data, dtype = np.int16)
        # ボリューム取得
        volume = np.abs(audio_data).mean()

        # 無音判定の閾値を下回ったかどうか
        if volume < THRESHOLD:
            silent_chunks += 1

        else:
            # チャンクリセット
            silent_chunks = 0

        if silent_chunks > int(RATE / CHUNK * SILENCE_DURATION):
            # Animationストップ
            socketio_emit.socketio_emit_stop_telop_animation()
            break

    # 録音終了
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(OUTPUT_FILE, 'wb') as wf:
        # チャンネル変更
        wf.setnchannels(CHANNELS)
        # フォーマット変更
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        # レート変更
        wf.setframerate(RATE)
        # フレーム変更
        wf.writeframes(b''.join(frames))

    # 作成したファイルパス取得
    saved_directory = os.path.abspath(OUTPUT_FILE)

    # パス返し
    return saved_directory