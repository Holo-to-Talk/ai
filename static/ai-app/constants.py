# テキスト
class TextSettings:
    QREVENT = "QRCodeを表示します"
    PHONEEVENT = "電話対応をご希望の場合、Spaceキーを押してください"
    PHONEEVENT2 = "駅員に電話をかけます"
    ENTEREVENT ="会話を終了する場合、Enterキーを押してください"
    CONVERSATIONEVENT = "会話を続けます"
    CONVERSATIONEVENT2 = "会話を終了します"
    ENTEREVENT2 = "Enterキーを押して始めてください"

# app.py
class AppSettings:
    # Time Sleep秒数
    TIME_SLEEP = 1
    # QRCode Time Sleepカウント
    QR_TIME_SLEEP_COUNT = 10
    # Time Sleepカウント
    TIME_SLEEP_COUNT = 5

# voice_Recording.py
class VoiceRecordingSettings:
    # チャンネル
    CHANNELS = 1
    # レート
    RATE = 44100
    # チャンク
    CHUNK = 1024
    # 出力ファイル名
    OUTPUT_FILE = "inputText.wav"
    # 無音判定の閾値
    THRESHOLD = 500
    # 録音終了秒数
    SILENCE_DURATION = 3

# audio_To_Text.py
class AudioToTextSettings:
    # モデル
    MODEL = "whisper-1"

# qr_code_found.py
class QRCodeFoundSettings:
    # 特定単語
    SEARCH_LIST = ['QRCode', 'QRコード', 'qrCode', 'qrコード', 'QR Code', 'QR コード', 'qr Code', 'qr コード']

# text_To_Audio.py
class TextToAudioSettings:
    # レート
    RATE = 150
    # ボリューム
    VOLUME = 1

# chatGPT_API_Output.py
class ChatGPTAPIOutputSettings:
    # モデル
    MODEL = "gpt-3.5-turbo"
    # トークン
    MAX_TOKENS = 100
    # プロンプト
    CHATGPT_SYSTEM_CONTENT = "日本語で対応してください"

# phoneAutomation.py
class PhoneAutomationSettings:
    # URL
    URL = "https://holog.net"
    # URL（開発）
    # URL = "https://num-0145.holog.net"
    # 代表電話番号
    PHONE_NUMBER = "+1 8302242800"
    # Driver Wait Time
    WEB_DRIVER_WAIT_TIME = 10
    # Time Sleep秒数
    TIME_SLEEP_TIME = 1