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
import text_To_Audio
import delete_Recording
import phoneAutomation

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

socketio.init_app(app)

TIME_SLEEP = AppSettings.TIME_SLEEP
QR_TIME_SLEEP_COUNT = AppSettings.QR_TIME_SLEEP_COUNT
TIME_SLEEP_COUNT = AppSettings.TIME_SLEEP_COUNT

flag_continuation =True
flag_space = False
flag_enter2 = False
conversation_history = []
conversation_input = ""
conversation_output = ""

def ai():
    savedDirectory = voice_Recording.voice_Recording()

    inputContent = audio_To_Text.audio_To_Text(savedDirectory)
    conversation_input = inputContent

    delete_Recording.delete_Recording(savedDirectory)

    global conversation_history
    if qr_code_found.qr_code_found(inputContent):
        outputContent = TextSettings.QREVENT
        conversation_output = outputContent
        socketio_emit.socketio_emit_output(outputContent)

        socketio_emit.socketio_emit_start_switching()
        text_To_Audio.text_To_Audio(outputContent)
        socketio_emit.socketio_emit_stop_switching()

        socketio_emit.socketio_emit_output_reset()

        socketio_emit.socketio_emit_image_qr_add_active()
        for count in range(QR_TIME_SLEEP_COUNT):
            socketio_emit.socketio_emit_countdown(QR_TIME_SLEEP_COUNT - count)
            time.sleep(TIME_SLEEP)
        socketio_emit.socketio_emit_countdown_reset()
        socketio_emit.socketio_emit_image_qr_remove_active()

    else:
        outputContent = chatGPT_API_Output.chatGPT_API_Output(conversation_history, inputContent)
        conversation_output = outputContent
        socketio_emit.socketio_emit_output(outputContent)

        socketio_emit.socketio_emit_start_switching()
        text_To_Audio.text_To_Audio(outputContent)
        socketio_emit.socketio_emit_stop_switching()

    outputContent = TextSettings.PHONEEVENT
    socketio_emit.socketio_emit_output(outputContent)

    socketio_emit.socketio_emit_start_switching()
    text_To_Audio.text_To_Audio(outputContent)
    socketio_emit.socketio_emit_stop_switching()

    global flag_space
    count = 0
    while True:
        if flag_space:
            socketio_emit.socketio_emit_countdown_reset()

            outputContent = TextSettings.PHONEEVENT2
            socketio_emit.socketio_emit_output(outputContent)

            socketio_emit.socketio_emit_start_switching()
            text_To_Audio.text_To_Audio(outputContent)
            socketio_emit.socketio_emit_stop_switching()

            phoneAutomation.phoneAutomation()
            break

        elif count == TIME_SLEEP_COUNT:
            socketio_emit.socketio_emit_countdown_reset()
            socketio_emit.socketio_emit_flag_space()
            flag_space = True
            break

        else:
            socketio_emit.socketio_emit_countdown(TIME_SLEEP_COUNT - count)
            time.sleep(TIME_SLEEP)
            count += 1

    outputContent = TextSettings.ENTEREVENT
    socketio_emit.socketio_emit_output(outputContent)

    socketio_emit.socketio_emit_start_switching()
    text_To_Audio.text_To_Audio(outputContent)
    socketio_emit.socketio_emit_stop_switching()

    global flag_continuation
    global flag_enter2
    count = 0
    while True:
        if flag_enter2:
            socketio_emit.socketio_emit_countdown_reset()

            conversation_history = []

            flag_continuation = False

            break

        elif count == TIME_SLEEP_COUNT:
            socketio_emit.socketio_emit_countdown_reset()

            conversation_history.append({"role": "user", "content": conversation_input})
            conversation_history.append({"role": "assistant", "content": conversation_output})

            flag_continuation = True

            socketio_emit.socketio_emit_flag_enter2()
            flag_enter2 = True

            break

        else:
            socketio_emit.socketio_emit_countdown(TIME_SLEEP_COUNT - count)
            time.sleep(TIME_SLEEP)
            count += 1

    socketio_emit.socketio_emit_flag_enter()
    flag_enter2 = False
    socketio_emit.socketio_emit_flag_enter2()
    flag_space = False
    socketio_emit.socketio_emit_flag_space()

    if flag_continuation:
        outputContent = TextSettings.CONVERSATIONEVENT
        socketio_emit.socketio_emit_output(outputContent)

        socketio_emit.socketio_emit_start_switching()
        text_To_Audio.text_To_Audio(outputContent)
        socketio_emit.socketio_emit_stop_switching()

        socketio_emit.socketio_emit_output_reset()

        socketio_emit.socketio_emit_telop_remove_display_none()
        socketio_emit.socketio_emit_telop_reset()

        socketio_emit.socketio_emit_flag_enter()
        socketio.start_background_task(target = ai)

    elif not flag_continuation:
        outputContent = TextSettings.CONVERSATIONEVENT2
        socketio_emit.socketio_emit_output(outputContent)

        socketio_emit.socketio_emit_start_switching()
        text_To_Audio.text_To_Audio(outputContent)
        socketio_emit.socketio_emit_stop_switching()

        socketio_emit.socketio_emit_output_reset()

        telopContent = TextSettings.ENTEREVENT2
        socketio_emit.socketio_emit_telop_remove_display_none()
        socketio_emit.socketio_emit_telop(telopContent)

@app.route('/home/')
def main():
    return render_template('index.html')

@socketio.on('enter_starting')
def handle_enter_event():
    socketio_emit.socketio_emit_flag_enter()

    socketio.start_background_task(target = ai)

@socketio.on('enter_conversation')
def handle_enter_event2():
    socketio_emit.socketio_emit_flag_enter2()

    global flag_enter2
    flag_enter2 = True

@socketio.on('space_phone')
def handle_space_event():
    socketio_emit.socketio_emit_flag_space()

    global flag_space
    flag_space = True

if __name__ == '__main__':
    socketio.run(app)