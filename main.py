from flask import Flask, request, abort, send_from_directory
from linebot import LineBotApi,WebhookHandler
from linebot.v3.messaging import MessagingApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, LocationMessage, LocationSendMessage, QuickReply, QuickReplyButton, LocationAction
from gemini import chat_with_loading,send_loading   # loading animation函數引入
from text_function import main_text, store, get_from_store
import os
from vision import vision
import dotenv
from weather_forecast import get_weather_forecast,get_city
from cloth_suggestion import cloth_suggestion
from farm import farm_advice

# setting
app = Flask(__name__)
dotenv.load_dotenv()

# 設定你的 LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
Ngrok = os.getenv("Ngrok_url")
print(Ngrok)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
messaging_api = MessagingApi(LINE_CHANNEL_ACCESS_TOKEN)

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
forcast = False
clothes = False
farm = False
pic = False

# message reply
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global if_need_address
    global forcast
    global clothes
    global farm
    global pic
    receive_text = event.message.text
    chat_id = event.source.user_id  # 提取 chat_id

    print(receive_text)
    if receive_text == "@天氣":
        pic = True
        message = TextSendMessage(text="請上傳一張天氣圖片")
        line_bot_api.reply_message(event.reply_token, message)
        return
    elif receive_text == "@天氣預報":
        send_loading(chat_id, 60)
        if_need_address = True
        forcast = True
        message = TextSendMessage(
                text="請分享你的位置",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=LocationAction(label="位置")
                        )
                    ]
                )
            )
    elif receive_text == "@服裝建議":
        send_loading(chat_id, 60)
        if_need_address = True
        clothes = True
        message = TextSendMessage(
                text="請分享你的位置",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=LocationAction(label="位置")
                        )
                    ]
                )
            )
    elif receive_text == "@農情資訊":
        send_loading(chat_id, 60)
        farm = True
        if_need_address = True
        message = TextSendMessage(
                text="請分享你的位置",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=LocationAction(label="位置")
                        )
                    ]
                )
            )
    else:
        send_loading(chat_id,60)
        res_text, is_main = main_text(receive_text)
        if not is_main:
            # 使用 chat_with_loading 進行回應並顯示動畫
            response = chat_with_loading(chat_id, res_text)
            message = TextSendMessage(text=response)
        else:
            if_need_address = True
            store(res_text)
            message = TextSendMessage(
                text="請分享你的位置",
                quick_reply=QuickReply(
                    items=[
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
    global forcast
    global clothes
    global farm
    if if_need_address == True:
        if forcast == True:
            address = event.message.address
            send_loading(event.source.user_id, 60)
            response = get_weather_forecast(address)
            message = TextSendMessage(text=response)
            line_bot_api.reply_message(event.reply_token, message)
            forcast = False
        elif clothes == True:
            address = event.message.address
            send_loading(event.source.user_id, 60)
            res = cloth_suggestion(get_city(address))
            print(res)
            res = chat_with_loading(event.source.user_id, res)
            message = TextSendMessage(text=res)
            line_bot_api.reply_message(event.reply_token, message)
            clothes = False
        elif farm == True:
            address = event.message.address
            send_loading(event.source.user_id, 60)
            response = farm_advice(address)
            message = TextSendMessage(text=response)
            line_bot_api.reply_message(event.reply_token, message)
            farm = False
        else:
            send_loading(event.source.user_id, 60)
            address = event.message.address
            res_text = get_from_store()
            res_text = res_text + address
            response = chat_with_loading(event.source.user_id, res_text)
            message = TextSendMessage(text=response)
            line_bot_api.reply_message(event.reply_token, message)
        if_need_address = False
    else:
        send_loading(event.source.user_id, 60)
        lon = event.message.longitude
        lat = event.message.latitude
        message = LocationSendMessage(
            title="你的位置",
            address=event.message.address,
            latitude=lat,
            longitude=lon
        )
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    global pic
    if pic == True:
        if not os.path.exists("image"):
            os.mkdir("image")
        message_content = line_bot_api.get_message_content(event.message.id)
        file_path = f"image/user_input.jpg"
        print(file_path)
        chat_id = event.source.user_id
        with open(file_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        prediction = vision(chat_id)
        print(prediction)
        res_text = main_text(prediction, predict=True)
        response = chat_with_loading(chat_id, res_text)
        message = TextSendMessage(text=response)
    elif pic == False:
        message = TextSendMessage(text="目前不支援天氣預報以外的圖片功能")
    pic = False
    line_bot_api.reply_message(event.reply_token, message)
    
if __name__ == "__main__":
    app.run() 