import google.generativeai as generativeai
import os
from dotenv import load_dotenv
import PIL.Image
from gemini import send_loading

load_dotenv()
api_key = os.getenv("gemini_api_key")

model = generativeai.GenerativeModel("gemini-2.0-flash-exp")
# 設定要傳給模型的圖片
def vision(chat_id):
    send_loading(chat_id, 5)
    try:
        image = PIL.Image.open("image/user_input.jpg")
        # 設定要傳給模型的文字提示
        prompts = "What weather is going to be.Try to give user som simple suggestions.Use zh-TW language."
        # 透過generate_content方法傳送圖片和文字提示給模型
        response = model.generate_content([prompts,image])
        return response.text
    except Exception as e:
        print(f"Error during vision: {e}")
        return "抱歉，發生錯誤，請稍後再試！"