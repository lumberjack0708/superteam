from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
import time
import threading

app = Flask(__name__)

# 設定 LINE 的 token 和 secret
LINE_CHANNEL_ACCESS_TOKEN = '你的 Channel Access Token'
LINE_CHANNEL_SECRET = '你的 Channel Secret'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def send_typing(event):
    """模擬 Line 的「打字中」效果"""
    try:
        # 讓 Line Bot 顯示「打字中」
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="打字中...")
        )
        # 等待模擬的處理時間
        time.sleep(3)  # 可以根據需要調整時間
        # 送出真正的訊息
        line_bot_api.push_message(
            event.source.user_id,
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
