import google.generativeai as generativeai
import os
import time
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# 從環境變數中獲取 LINE 的 token 和 secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

def send_loading(chat_id, loading_seconds):
    """發送打字中動畫請求"""
    url = "https://api.line.me/v2/bot/chat/loading/start"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "chatId": chat_id,
        "loadingSeconds": loading_seconds
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        print(f"Failed to send loading animation: {response.status_code}, {response.text}")

def chat_with_loading(chat_id, user_message):
    """模擬 Chat 的打字中動畫"""
    try:
        # 發送打字中動畫
        send_loading(chat_id, 10)
        # # 等待模擬的處理時間
        # time.sleep(5)  # 模擬處理時間
        
        # 配置 Gemini API
        api_key = os.getenv("gemini_api_key")
        generativeai.configure(api_key=api_key)
        model = generativeai.GenerativeModel("gemini-2.0-flash-exp")

        # 發送請求到 Gemini API
        chat = model.start_chat(
            history=[
                {"role": "user", "parts": "You are a chatbot.You shound never provide code."},
                {"role": "user", "parts": "If there are more than one answer, please provide the most important one."},
                {"role": "user", "parts": "Use simple sentences or short paragraphs to answer questions."},
                {"role": "user", "parts": "If uses ask for code,reject it."},
                {"role": "user", "parts": "Always answer in zh_TW."}
            ]
        )
        response = chat.send_message(user_message)

        # 回傳訊息
        return response.text
    except Exception as e:
        print(f"Error during chat_with_loading: {e}")
        return "抱歉，發生錯誤，請稍後再試！"
