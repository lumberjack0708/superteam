# 程式碼測試區

from text_function import get_specia_reply,main_text
from gemini import chat_with_loading
from weather_forecast import get_weather_forecast
from URL_load import scrape_data
import re

# xpath = "/html/body/div[3]/main/div[1]/div[2]/div[2]/div/div/ol/li[*]/a/span[position()=1]|/html/body/div[3]/main/div[1]/div[2]/div[2]/div/div/ol/li[*]/a/span[2]/span/span[1]"
# url = "https://www.cwa.gov.tw/V8/C/W/County/index.html"
# print(scrape_data(url, xpath))
print(main_text("@颱風假"))