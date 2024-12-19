from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from socketio_Config import socketio
from dotenv import load_dotenv
from constants import AppSettings, TextSettings
import os
import time

import socketio_emit
import voice_Recording
import audio_To_Text
import qr_code_found
import chatGPT_API_Output
import text_To_Audio_Animation
import delete_Recording
import phoneAutomation

app = Flask(__name__)

# .env
load_dotenv()
# SECRET Key取得
app.secret_key = os.getenv("SECRET_KEY")

socketio.init_app(app)

# Time Sleep秒数取得
TIME_SLEEP = AppSettings.TIME_SLEEP
# QR用Time Sleep取得
QR_TIME_SLEEP_COUNT = AppSettings.QR_TIME_SLEEP_COUNT
# Time Sleepカウント取得
TIME_SLEEP_COUNT = AppSettings.TIME_SLEEP_COUNT

# 会話用FLag
flag_continuation =True
# Space用Flag
flag_space = False
# Enter用Flag
flag_enter2 = False
# 会話
conversation_history = []
# 入力会話
conversation_input = ""
# 出力
conversation_output = ""

def ai():
    # ボイス録音・作成したファイルのディレクトリ取得
    savedDirectory = voice_Recording.voice_Recording()

    # ボイスをテキストに変換・取得
    inputContent = audio_To_Text.audio_To_Text(savedDirectory)
    # 会話保存用に保管
    conversation_input = inputContent

    # 作成したファイルの削除
    delete_Recording.delete_Recording(savedDirectory)

    global conversation_history
    # 入力値に特定の単語があるか
    if qr_code_found.qr_code_found(inputContent):
        # テキスト取得
        outputContent = TextSettings.QREVENT
        # 会話保存用に保管
        conversation_output = outputContent
        # テキスト出力
        socketio_emit.socketio_emit_output(outputContent)
        # Animation・音声出力
        text_To_Audio_Animation.text_To_Audio_Animation(outputContent)

        # テキスト削除
        socketio_emit.socketio_emit_output_reset()
        # QRCode表示
        socketio_emit.socketio_emit_image_qr_add_active()
        # 秒数カウント
        for count in range(QR_TIME_SLEEP_COUNT):
            socketio_emit.socketio_emit_countdown(QR_TIME_SLEEP_COUNT - count)
            time.sleep(TIME_SLEEP)
        # カウント削除
        socketio_emit.socketio_emit_countdown_reset()
        # QRCode削除
        socketio_emit.socketio_emit_image_qr_remove_active()

    else:
        # テキスト取得
        outputContent = chatGPT_API_Output.chatGPT_API_Output(conversation_history, inputContent)
        # 会話保存用に保管
        conversation_output = outputContent
        # テキスト出力
        socketio_emit.socketio_emit_output(outputContent)
        # Animation・音声出力
        text_To_Audio_Animation.text_To_Audio_Animation(outputContent)

    # テキスト取得
    outputContent = TextSettings.PHONEEVENT
    # テキスト出力
    socketio_emit.socketio_emit_output(outputContent)
    # Animation・音声出力
    text_To_Audio_Animation.text_To_Audio_Animation(outputContent)

    global flag_space
    count = 0
    while True:
        # Spaceが押されたかどうか
        if flag_space:
            # カウント削除
            socketio_emit.socketio_emit_countdown_reset()

            # テキスト取得
            outputContent = TextSettings.PHONEEVENT2
            # テキスト出力
            socketio_emit.socketio_emit_output(outputContent)
            # Animation・音声出力
            text_To_Audio_Animation.text_To_Audio_Animation(outputContent)

            # 電話をかける（バックグラウンド）
            phoneAutomation.phoneAutomation()

            break

        # カウントが終わったかどうか
        elif count == TIME_SLEEP_COUNT:
            # カウント削除
            socketio_emit.socketio_emit_countdown_reset()

            # Flag変更
            socketio_emit.socketio_emit_flag_space()
            flag_space = True

            break

        else:
            # 秒数カウント
            socketio_emit.socketio_emit_countdown(TIME_SLEEP_COUNT - count)
            time.sleep(TIME_SLEEP)
            count += 1

    # テキスト取得
    outputContent = TextSettings.ENTEREVENT
    # テキスト出力
    socketio_emit.socketio_emit_output(outputContent)
    # Animation・音声出力
    text_To_Audio_Animation.text_To_Audio_Animation(outputContent)

    global flag_continuation
    global flag_enter2
    count = 0
    while True:
        # Enterが押されたかどうか
        if flag_enter2:
            # カウント削除
            socketio_emit.socketio_emit_countdown_reset()

            # 会話削除
            conversation_history = []

            # Flag変更
            flag_continuation = False

            break

        # カウントが終わったかどうか
        elif count == TIME_SLEEP_COUNT:
            # カウント削除
            socketio_emit.socketio_emit_countdown_reset()

            # 会話保存
            conversation_history.append({"role": "user", "content": conversation_input})
            conversation_history.append({"role": "assistant", "content": conversation_output})

            # Flag変更
            flag_continuation = True
            socketio_emit.socketio_emit_flag_enter2()
            flag_enter2 = True

            break

        else:
            # 秒数カウント
            socketio_emit.socketio_emit_countdown(TIME_SLEEP_COUNT - count)
            time.sleep(TIME_SLEEP)
            count += 1

    # Flagリセット
    socketio_emit.socketio_emit_flag_enter()
    flag_enter2 = False
    socketio_emit.socketio_emit_flag_enter2()
    flag_space = False
    socketio_emit.socketio_emit_flag_space()

    # 会話を続ける
    if flag_continuation:
        # テキスト取得
        outputContent = TextSettings.CONVERSATIONEVENT
        # テキスト出力
        socketio_emit.socketio_emit_output(outputContent)
        # Animation・音声出力
        text_To_Audio_Animation.text_To_Audio_Animation(outputContent)

        # テキスト削除
        socketio_emit.socketio_emit_output_reset()

        # テロップ表示
        socketio_emit.socketio_emit_telop_remove_display_none()
        # テロップ削除
        socketio_emit.socketio_emit_telop_reset()

        # Flag変更
        socketio_emit.socketio_emit_flag_enter()
        # メイン処理再始動
        socketio.start_background_task(target = ai)

    # 会話を続けない
    elif not flag_continuation:
        # テキスト取得
        outputContent = TextSettings.CONVERSATIONEVENT2
        # テキスト出力
        socketio_emit.socketio_emit_output(outputContent)
        # Animation・音声出力
        text_To_Audio_Animation.text_To_Audio_Animation(outputContent)

        # テキスト削除
        socketio_emit.socketio_emit_output_reset()

        # テキスト取得
        telopContent = TextSettings.ENTEREVENT2
        # テロップ表示
        socketio_emit.socketio_emit_telop_remove_display_none()
        # テロップ削除
        socketio_emit.socketio_emit_telop(telopContent)

# App Route (/home)
@app.route('/home/')
def main():
    # index.htmlの表示
    return render_template('index.html')

# Enterが押されたら
@socketio.on('enter_starting')
def handle_enter_event():
    # Flag変更
    socketio_emit.socketio_emit_flag_enter()

    # メイン処理始動
    socketio.start_background_task(target = ai)

# Enterが押されたら
@socketio.on('enter_conversation')
def handle_enter_event2():
    # Flag変更
    socketio_emit.socketio_emit_flag_enter2()
    global flag_enter2
    flag_enter2 = True

# Spaceが押されたら
@socketio.on('space_phone')
def handle_space_event():
    # Flag変更
    socketio_emit.socketio_emit_flag_space()
    global flag_space
    flag_space = True

# FLask起動
if __name__ == '__main__':
    socketio.run(app)