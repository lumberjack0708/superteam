import google.generativeai as generativeai
import os
from dotenv import load_dotenv

load_dotenv()

# Set the API key
api_key = os.getenv("gemini_api_key")
generativeai.configure(api_key=api_key)
model = generativeai.GenerativeModel("gemini-2.0-flash-exp")

def chat(text):
    chat = model.start_chat(
    # 在gemini-2.0-flash-exp模型中，設定role參數為user，代表使用者的身分，由於不支援system身分，所以暫時用user代替
    # 使用history參數來設定對話的歷史紀錄，可以通過輸入歷史紀錄對chat做設定
        history=[
            {"role":  "user", "parts": "If there are more than one answer, please provide the most important one."},
            {"role": "user", "parts": "Use single sentences or short paragraphs to answer questions."},
            # 設定回答者只會用zh_TW回答
            {"role": "user", "parts": "Always answer in zh_TW."}
        ]
    )

    # 在send_message中同樣可以將stream參數設定為True，啟用串流模式
    response = chat.send_message(text)
    return response.text

print(chat("What is the capital of Taiwan?"))