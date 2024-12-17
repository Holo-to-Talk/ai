class TextSettings:
    QREVENT = "QRCodeを表示します"
    PHONEEVENT = "電話対応をご希望の場合、Spaceキーを押してください"
    PHONEEVENT2 = "駅員に電話をかけます"
    ENTEREVENT ="会話を終了する場合、Enterキーを押してください"
    CONVERSATIONEVENT = "会話を続けます"
    CONVERSATIONEVENT2 = "会話を終了します"
    ENTEREVENT2 = "Enterキーを押して始めてください"

class AppSettings:
    TIME_SLEEP = 1
    QR_TIME_SLEEP_COUNT = 10
    TIME_SLEEP_COUNT = 5

class VoiceRecordingSettings:
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    OUTPUT_FILE = "inputText.wav"
    THRESHOLD = 500
    SILENCE_DURATION = 3

class AudioToTextSettings:
    MODEL = "whisper-1"

class QRCodeFoundSettings:
    SEARCH_LIST = ['QRCode', 'QRコード', 'qrCode', 'qrコード', 'QR Code', 'QR コード', 'qr Code', 'qr コード']

class TextToAudioSettings:
    RATE = 150
    VOLUME = 1

class ChatGPTAPIOutputSettings:
    MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 100

class PhoneAutomationSettings:
    URL = "https://holog.net"
    # URL = "https://num-0145.holog.net"
    PHONE_NUMBER = "+1 8302242800"
    WEB_DRIVER_WAIT_TIME = 10
    TIME_SLEEP_TIME = 1