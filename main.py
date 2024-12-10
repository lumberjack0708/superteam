from flask import Flask, request, abort,send_from_directory
from linebot import LineBotApi, WebhookHandler
from linebot.v3.messaging import MessagingApi  # 更改：導入新的 MessagingApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageMessage,LocationMessage,LocationSendMessage,QuickReply,QuickReplyButton,LocationAction
from gpt import get_text
from text_function import main_text,get_store
import os
import time
from dotenv import load_dotenv
from record_image import record_image
from vision import vision

# setting
app = Flask(__name__)
load_dotenv()
# 設定你的 LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
Ngrok = os.getenv("Ngrok_url")
print(Ngrok)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
messaging_api = MessagingApi(LINE_CHANNEL_ACCESS_TOKEN)  # 更改：初始化新的 MessagingApi

@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求來自 LINE 平台
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory('image', filename)

if_need_address = False
# message reply
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global if_need_address
    #傳送文字訊息
    receive_text = event.message.text
    print(receive_text)
    res_text, is_main = main_text(receive_text)
    if is_main == False:
        gpt_text = get_text(res_text)
        message = TextSendMessage(text=gpt_text)
    else:
        if_need_address = True
        message = TextSendMessage(
            text = "請分享你的位置",
            quick_reply=QuickReply(
                items = [
                    QuickReplyButton(
                        action=LocationAction(label="位置")
                    )
                ]
            )
        )
    
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    global if_need_address
    if if_need_address == True:
        address = event.message.address
        store_text = get_store()
        text = f"使用者的問題及已取得的相關資訊:{store_text};\n使用者的位置:{address};\n幫我生成簡單回應並給予建議"
        gpt_text = get_text(text)
        message = TextSendMessage(text=gpt_text)
        line_bot_api.reply_message(event.reply_token, message)
    else:
        lon = event.message.longitude
        lat = event.message.latitude
        message = LocationSendMessage(
            title = "你的位置",
            address = event.message.address,
            latitude = lat,
            longitude = lon
        )
        line_bot_api.reply_message(event.reply_token, message)
    
        
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    if not os.path.exists("image"):
        os.mkdir("image")
    message_content = line_bot_api.get_message_content(event.message.id)
    file_path = f"image/user_input.jpg"
    print(file_path)
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    record_image()
    pediction = vision()
    print(pediction)
    res_text = main_text(pediction,predict=True)
    gpt_text = get_text(res_text)
    message = TextSendMessage(text=gpt_text)
    line_bot_api.reply_message(event.reply_token, message)



if __name__ == "__main__":
    app.run()