import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import json
import dotenv
import os
import google.generativeai as generativeai



dotenv.load_dotenv()
generativeai.configure(api_key=os.getenv("gemini_api_key"))

def get_farm_info():
    url = "https://www.cwa.gov.tw/V8/C/L/agriculture.html"
    xpath = "/html/body/div[3]/main/div/div[3]/div[1]/div[2]/div"

    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=option)

    try:
        driver.get(url)
        driver.implicitly_wait(10)
        element = driver.find_element(By.XPATH, xpath)
        inf = {}
        text_content = driver.execute_script("return arguments[0].textContent;", element)
        for line in text_content.split("\n"):
            if line.strip():
                if re.findall(r"地區", line):
                    region = line.strip()
                    region = region.replace("'","")
                    inf[region] = []
                else:
                    line_inf = line.strip().replace("'" , "")
                    inf[region].append(line_inf)
    except NoSuchElementException:
        print("Element not found")
    finally:
        driver.quit()
        return inf
    
with open("degree_day.json", "r" , encoding="utf-8") as f:
    advice = f.read()
    advice = json.loads(advice)
    advice = advice["advice_segments"]

area = {
    "台北市": "北部地區",
    "新北市": "北部地區",
    "基隆市": "北部地區",
    "桃園市": "北部地區",
    "新竹市": "北部地區",
    "新竹縣": "北部地區",
    "宜蘭縣": "東北部地區",
    "台中市": "中部地區",
    "苗栗縣": "中部地區",
    "彰化縣": "中部地區",
    "南投縣": "中部地區",
    "雲林縣": "中部地區",
    "嘉義市": "南部地區",
    "嘉義縣": "南部地區",
    "台南市": "南部地區",
    "高雄市": "南部地區",
    "屏東縣": "南部地區",
    "花蓮縣": "東部地區",
    "台東縣": "東部地區",
    "澎湖縣": "離島地區",
    "金門縣": "離島地區",
    "連江縣": "離島地區"
}
def extract_city_from_address(address):
    # 遍歷縣市列表，檢查每個縣市名稱是否在地址中
    for city in area:
        if city in address:
            return city
    return None  # 如果未找到匹配的縣市，返回 None

inf = get_farm_info()

def get_advice(area_info, advice):
    model = generativeai.GenerativeModel("gemini-2.0-flash-exp")
    prompts = f"根據{area_info}的農業資訊，及{advice}中的內容，請給我一些關於農業的建議。用text格式不要使用markdown語法。並確保使用zh-TW語言。" 
    content = model.generate_content(prompts)
    return content.text

def farm_advice(address):
    inf_list = list(inf.keys())
    if extract_city_from_address(address) is None:
        return "目前僅提供台灣本島的農業資訊，暫無您查詢地區的資訊"
    elif area[extract_city_from_address(address)] not in inf_list:
        return "目前僅提供台灣本島的農業資訊，暫無您查詢地區的資訊"
    return get_advice(inf[area[extract_city_from_address(address)]], advice)
