import re
from db import *

# バリデーション関数
def validate_name(name):
    if not name:
        return "駅名を入力してください。"
    return ""

def validate_station_num(station_num):
    if not station_num.encode('utf-8').isalnum():
        return "駅番号は半角英数字のみを入力してください。"
    if len(station_num) > 5:
        return "駅番号は5文字以下で入力してください。"
    
    try:
        # データベース接続とクエリ実行
        cursor = mysql.connection.cursor()
        cursor.execute(''' use holo_to_talk ''')
        query = "SELECT COUNT(*) FROM station_info WHERE station_num = %s"
        cursor.execute(query, (station_num,))
        count = cursor.fetchone()[0]

        if count > 0:
            return f"駅番号「{station_num}」はすでに登録されています。"

    except Exception as e:
        return f"データベースエラー: {e}"

    finally:
        # カーソルを閉じる
        cursor.close()

    return ""

def validate_address(address):
    if not address:
        return "駅の住所を入力して下さい。"
    return ""

def validate_phone_num(phone_num):
    # 電話番号が+で始まり、12文字であることを確認する正規表現
    pattern = r"^\+[0-9]{11}$"
    if not re.match(pattern, phone_num):
        return "電話番号が無効です。フォーマットは「+」を含めた12文字にしてください。"
    return ""

def validate_app_sid(app_sid):
    if not app_sid.encode('utf-8').isalnum():
        return "twilio_twiml_app_sidは半角英数字のみを入力してください。"
    if len(app_sid) != 34:
        return "twilio_twiml_app_sidは半角英数字34文字です。"
    return ""

def validate_app_key(app_key):
    if not app_key.encode('utf-8').isalnum():
        return "api_keyは半角英数字のみを入力してください。"
    if len(app_key) != 34:
        return "api_keyは半角英数字34文字です。"
    return ""

def validate_app_secret(app_secret):
    if not app_secret.encode('utf-8').isalnum():
        return "api_secretは半角英数字のみを入力してください。"
    if len(app_secret) != 32:
        return "api_secretは半角英数字32文字です。"
    return ""

def validate_password(password):
    if len(password) < 5:
        return "パスワードは5文字以上で入力して下さい。"
    return ""