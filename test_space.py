# 程式碼測試區
from text_function import get_specia_reply,main_text
from gemini import chat_with_loading
from weather_forecast import get_weather_forecast
from URL_load import scrape_data
from set_new_key import set_new_key
import re

# url = "https://airtw.moenv.gov.tw/CHT/Forecast/Forecast_3days.aspx"
# xpath = "/html/body/form/div[4]/main/div/div[2]/div[2]/div[3]"
# key = "@空氣品質"
# set_new_key(key,url,xpath)
print(get_specia_reply("@氣溫"))