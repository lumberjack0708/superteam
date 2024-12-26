# 程式碼測試區
from text_function import get_specia_reply,main_text
from gemini import chat_with_loading
from weather_forecast import get_weather_forecast
from URL_load import scrape_data
from set_new_key import set_new_key
import re

url = "https://www.cwa.gov.tw/V8/C/P/Typhoon/TY_NEWS.html"
xpath = "/html/body/div[3]/main/div/div/div"
key = "@颱風消息"
set_new_key(key,url,xpath)