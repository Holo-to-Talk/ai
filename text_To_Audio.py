import pyttsx3
from constants import TextToAudioSettings

# 音声出力
def text_To_Audio(outputContent):
    # レート取得
    RATE = TextToAudioSettings.RATE

    # ボリューム取得
    VOLUME = TextToAudioSettings.VOLUME

    # エンジン
    engine = pyttsx3.init()

    # レート指定
    engine.setProperty('rate', RATE)

    # ボリューム指定
    engine.setProperty('volume', VOLUME)

    # テキスト取得
    text = outputContent

    # テキスト指定
    engine.say(text)

    # エンジン起動・待機
    engine.runAndWait()