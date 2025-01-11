import openai
from dotenv import load_dotenv
from constants import AudioToTextSettings
import os

import socketio_emit

# 音声からテキスト取得
def audio_To_Text(savedDirectory):
    # .env
    load_dotenv()

    # API Key取得
    API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = API_KEY

    # モデル取得
    MODEL = AudioToTextSettings.MODEL

    # 作成したファイルパス取得
    audio_file_path = savedDirectory

    with open(audio_file_path, 'rb') as audio_file:
        # テキスト化
        transcription = openai.Audio.transcribe(MODEL, audio_file)

        # テキスト取得
        inputContent = transcription['text']
        # テロップ削除
        socketio_emit.socketio_emit_telop_add_display_none()
        # 入力値出力
        socketio_emit.socketio_emit_input(inputContent)

        # 開発用（質問内容の固定）
        #inputContent = ""

        # 開発用（質問内容の確認）
        #print(inputContent)

        # テキスト返し
        return inputContent