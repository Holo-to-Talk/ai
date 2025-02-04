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

    # モデル名取得
    MODEL = ChatGPTAPIOutputSettings.MODEL

    # ランダム性の制御の取得
    TEMPERATURE = ChatGPTAPIOutputSettings.TEMPERATURE

    # 生成される単語の確率の制御の取得
    TOP_P = ChatGPTAPIOutputSettings.TOP_P

    # 新しいアイデアやトピックの制御の取得
    PRESENCE_PENALTY = ChatGPTAPIOutputSettings.PRESENCE_PENALTY

    # 同じ単語やフレーズを減らす制御の取得
    FREQUENCY_PENALTY = ChatGPTAPIOutputSettings.FREQUENCY_PENALTY

    # トークン最大値取得
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
        # ランダム性
        temperature = TEMPERATURE,

        # 生成される単語の確率
        top_p = TOP_P,

        # 新しいアイデアやトピック
        presence_penalty = PRESENCE_PENALTY,

        # 同じ単語やフレーズ
        frequency_penalty = FREQUENCY_PENALTY,

        # モデル
        model = MODEL,

        # メッセージ
        messages = messages,

        # トークン
        max_tokens = MAX_TOKENS,
    )

    # テキスト取得
    outputContent = response['choices'][0]['message']['content']

    # 開発用（回答内容の固定）
    # outputContent = ""

    # 開発用（回答内容の表示）
    print(outputContent)

    # テキスト返し
    return outputContent