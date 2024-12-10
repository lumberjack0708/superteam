import google.generativeai as generativeai
import os
from dotenv import load_dotenv
import PIL.Image

load_dotenv()
api_key = os.getenv("gemini_api_key")

model = generativeai.GenerativeModel("gemini-2.0-flash-exp")
# 設定要傳給模型的圖片
def vision():
    image = PIL.Image.open("image/user_input.jpg")
    # 設定要傳給模型的文字提示
    prompts = "What weather is going to be.Use zh-TW language."
    # 透過generate_content方法傳送圖片和文字提示給模型
    response = model.generate_content([prompts,image])
    return response.text