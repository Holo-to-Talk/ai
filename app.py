import os
import re
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, redirect, request, render_template, session, url_for
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import Dial, VoiceResponse
import bcrypt
from db import *
from validation import *

# ai
from flask_socketio import SocketIO, emit
from socketio_Config import socketio
from constants import AppSettings, TextSettings
import time

import socketio_emit
import voice_Recording
import audio_To_Text
import qr_code_found
import chatGPT_API_Output
import text_To_Audio_Animation
import delete_Recording
import phoneAutomation

# .envファイルから環境変数を読み込む
load_dotenv()

# Flaskアプリケーションを作成
app = Flask(__name__,template_folder='./static/')
app.secret_key = os.environ.get("SECRET_KEY")

# ai
socketio.init_app(app)

# 特殊文字やアンダースコアを除去する正規表現
alphanumeric_only = re.compile("[\W_]+")

# 電話番号の形式を検証するための正規表現
phone_pattern = re.compile(r"^[\d\+\-\(\) ]+$")

# Twilioの電話番号を環境変数から取得
twilio_number = os.environ.get("TWILIO_CALLER_ID")

# 最新のユーザーIDをメモリに保存する辞書
IDENTITY = {"identity": ""}

# トークンを生成して返すAPIエンドポイント
@app.route("/token", methods=["GET"])
def token():
    # 日本語コメント: セッションからTwilioのアカウント情報を取得
    twilio_config = session.get('twilio')
    if not twilio_config:
        return jsonify({"error": "Twilio configuration not found in session"}), 403

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    application_sid = twilio_config["app_sid"]
    api_key = twilio_config["app_key"]
    api_secret = twilio_config["app_secret"]

    # 日本語コメント: sessionからphone_numを取得してtwilio_numberに格納
    twilio_number = twilio_config.get("phone_num", "")
    if not twilio_number:
        return jsonify({"error": "Twilio phone number not found in session"}), 403

    print("Twilio Number from Session:", twilio_number)
    print(application_sid)
    print(api_key)
    print(api_secret)

    # ランダムなユーザー名を生成し、記号を削除してIDとして保存
    identity = twilio_number
    IDENTITY["identity"] = identity

    # アクセストークンを生成し、ユーザーIDを設定
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Voice Grantを作成し、トークンに追加（着信許可）
    voice_grant = VoiceGrant(
        outgoing_application_sid=application_sid,
        incoming_allow=True,
    )
    token.add_grant(voice_grant)

    # トークンをJWT形式に変換
    token = token.to_jwt()

    # トークンとユーザーIDをJSON形式で返す
    return jsonify(identity=identity, token=token)

# ルートURLにアクセスされた際の処理
@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html')
    return redirect('/station/login')

# ログイン処理
@app.route('/station/login', methods=['GET', 'POST'])
def login():
    error_msg = ""  # エラーメッセージを初期化

    if request.method == 'GET':
        # 日本語コメント: ユーザーが既にログインしている場合はトップページにリダイレクト
        if 'user' in session:
            return redirect("/")
        else:
            return render_template('./station/login.html', error_msg=error_msg)

    if request.method == 'POST':
        num = request.form.get('num', '')  # 日本語コメント: フォームから station_num を取得
        password = request.form.get('password', '')  # 日本語コメント: フォームからパスワードを取得

        # 日本語コメント: データベース接続を開始
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute('''USE holo_to_talk''')  # データベースを選択

        # 日本語コメント: station_num に基づいてユーザー情報を取得
        query = "SELECT * FROM users WHERE station_num = %s"
        cursor.execute(query, (num,))
        users = cursor.fetchall()

        if len(users) == 1:
            user = users[0]

            # 日本語コメント: パスワードの照合
            if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):  # user[2] がハッシュ化されたパスワードと仮定
                session['user'] = user[0]  # セッションにユーザーIDを保存

                # 日本語コメント: station_num を基に Twilio の情報を取得
                query = """
                SELECT station_info.app_sid, station_info.app_key, station_info.app_secret,station_info.phone_num
                FROM station_info
                INNER JOIN users ON station_info.station_num = users.station_num
                WHERE users.station_num = %s;
                """

                cursor.execute(query, (num,))
                twilio_config = cursor.fetchone()
                print(twilio_config)
                if twilio_config:
                    print(twilio_config)
                    session['twilio'] = {
                        "app_sid": twilio_config[0],
                        "app_key": twilio_config[1],
                        "app_secret": twilio_config[2],
                        "phone_num": twilio_config[3]
                    }

                return redirect('/')
            else:
                error_msg = "ログインエラー: IDまたはパスワードが間違っています"
        else:
            error_msg = "ログインエラー: IDまたはパスワードが間違っています"

        # 日本語コメント: エラーメッセージを渡してログインページを再表示
        return render_template('./station/login.html', error_msg=error_msg)

# ai
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
    # home.htmlの表示
    return render_template('home.html')

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

# アプリケーションを実行
if __name__ == "__main__":
    app.run(debug=True)