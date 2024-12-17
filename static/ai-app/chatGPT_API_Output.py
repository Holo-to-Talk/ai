import openai
from dotenv import load_dotenv
from constants import ChatGPTAPIOutputSettings
import os

def chatGPT_API_Output(conversation_history, inputContent):
    load_dotenv()

    API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = API_KEY

    MODEL = ChatGPTAPIOutputSettings.MODEL

    MAX_TOKENS = ChatGPTAPIOutputSettings.MAX_TOKENS

    if conversation_history:
        conversation_history.append({"role": "user", "content": inputContent})
        messages = conversation_history

    else:
        messages = [
            {"role": "user", "content": inputContent}
        ]

    response = openai.ChatCompletion.create(
        model = MODEL,

        messages = messages,

        max_tokens = MAX_TOKENS,

        temperature = 0.7,
    )

    outputContent = response['choices'][0]['message']['content']

    return outputContent