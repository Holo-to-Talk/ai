import socketio_emit
import text_To_Audio

# 画像切替・音声出力
def text_To_Audio_Animation(outputContent):
    # 画像切替スタート
    socketio_emit.socketio_emit_start_switching()
    # 音声出力
    text_To_Audio.text_To_Audio(outputContent)
    # 画像切替ストップ
    socketio_emit.socketio_emit_stop_switching()