# 這是一份loading animation的範例程式碼，當用戶發送訊息時，會先發送打字中動畫，然後再回覆訊息。
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
import time
import threading
import os  # 引入 os 模組
import requests  # 用於發送 HTTP 請求
import json

app = Flask(__name__)

# 從環境變數中獲取 LINE 的 token 和 secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 確保 token 和 secret 都已正確配置
if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("LINE_CHANNEL_ACCESS_TOKEN 或 LINE_CHANNEL_SECRET 未正確配置")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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


def send_typing(event):
    """模擬 Line 的「打字中」效果並覆蓋結果"""
    try:
        # 取得 chatId
        chat_id = event.source.user_id
        # 發送打字中動畫
        send_loading(chat_id, 5)
        # 等待模擬的處理時間
        time.sleep(5)  # 可以根據需要調整時間
        # 送出真正的訊息
        line_bot_api.push_message(
            chat_id,
            TextSendMessage(text="處理完成，這是回應內容！")
        )
    except Exception as e:
        print(f"發送失敗: {e}")

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 使用多執行緒模擬「打字中」
    threading.Thread(target=send_typing, args=(event,)).start()

if __name__ == "__main__":
    app.run()
