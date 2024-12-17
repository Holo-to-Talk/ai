from flask import Flask
from flask_mysql_connector import MySQL
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# MySQL設定
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_PORT'] = (os.getenv('MYSQL_PORT'))

mysql = MySQL(app)

def db_connection():
    # MySQL接続チェック用のデバッグ
    if mysql.connection is None:
        print("MySQLへの接続に失敗しました。設定情報を確認してください。")
        return None  # 接続失敗時はNoneを返す

    try:
        # データベース接続を返却
        conn = mysql.connection
        conn.ping(reconnect=True)  # 接続確認のため再接続をチェック
        return conn
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None  # エラー時もNoneを返す
