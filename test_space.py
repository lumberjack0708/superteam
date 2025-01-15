# 程式碼測試區
from text_function import get_specia_reply,main_text
from gemini import chat_with_loading
from weather_forecast import get_weather_forecast
from URL_load import scrape_data
from set_new_key import set_new_key
import re
import os


api_key = os.getenv("gemini_api_key")
print(api_key)