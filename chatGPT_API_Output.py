import openai
from dotenv import load_dotenv
from constants import ChatGPTAPIOutputSettings
import os

# ChatGPTからの返答
def chatGPT_API_Output(conversation_history, inputContent):
    # .env
    load_dotenv()

    # API Key取得
    API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = API_KEY

    # モデル取得
    MODEL = ChatGPTAPIOutputSettings.MODEL

    # トークン取得
    MAX_TOKENS = ChatGPTAPIOutputSettings.MAX_TOKENS

    # プロンプト取得
    SYSTEM_CONTENT = ChatGPTAPIOutputSettings.CHATGPT_SYSTEM_CONTENT

    # 会話があるかどうか
    if conversation_history:
        # メッセージ追加
        conversation_history.append({"role": "user", "content": inputContent})
        messages = conversation_history

    else:
        # メッセージ作成
        messages = [
            {"role": "system", "content": SYSTEM_CONTENT},
            {"role": "user", "content": inputContent}
        ]

    response = openai.ChatCompletion.create(
        # モデル
        model = MODEL,

        # メッセージ
        messages = messages,

        # トークン
        max_tokens = MAX_TOKENS,

        # 創造性
        temperature = 0.7,
    )

    # テキスト取得
    outputContent = response['choices'][0]['message']['content']

    # テキスト返し
    return outputContent