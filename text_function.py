import re
import json
import time
from datetime import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver

with open ('keyword_url.json','r',encoding='utf-8') as f:
    url_dict = f.read()
    #轉為python
    url_dict = json.loads(url_dict)

with open ('keyword.json','r',encoding='utf-8') as f:
    url_list = f.read()
    url_list = json.loads(url_list)

# 關鍵詞辨認及回復相關資訊
def main_text(text,predict=False):
    if predict == True:
        return f"使用者的問題:當下天氣狀況;\n預測結果:{text};\n幫我生成簡單回應並給予建議"
    else:
        is_get = False
        for i in range(len(url_list)):
            if re.search(url_list[i],text):
                is_get = True
                result = url_list[i]
                break
        if is_get == True:
            refresh = time_space(get_info_from_json(result))
            if refresh == True:
                res = get_specia_reply(result)
                res = cobi_test(text,result,res)
                return res,is_get
            else:
                res = get_info(result)
                res = cobi_test(text,result,res)
                return res,is_get
        else:
            print(f"return message: {text}")
            res = text
            return res,is_get

# 關鍵詞搜索及爬蟲資料儲存   
def get_specia_reply(key):
    from URL_load import scrape_data
    url = url_dict[key][0]
    xpath = url_dict[key][1]
    re_inf = scrape_data(url,xpath)
    # print(f"已取得資訊{re_inf}")
    information_store = get_from_json()
    information_store[key]["info"] = re_inf
    information_store[key]["time"] = time.strftime("%Y-%m-%d %H:%M")
    store_to_json(information_store)
    return re_inf

def cobi_test(text,key,info):
    return f"使用者的問題:{text};\n以下是目前已知的{key}資訊：\n{info}。\n幫我以一般人類對話的方式回應"

def store(text):
    with open('store.txt','w',encoding='utf-8') as f:
        f.write(text)
        f.close()

# 時間間隔判斷
def time_space(info:dict):
    need = False
    t1 = info["time"]
    space = info["space"]
    time.sleep(1)
    t2 = time.strftime("%Y-%m-%d %H:%M")
    t1 = datetime.strptime(t1, "%Y-%m-%d %H:%M")
    t2 = datetime.strptime(t2, "%Y-%m-%d %H:%M")
    t_diff = t2 - t1
    t_minute = int(t_diff.total_seconds()/60)
    if t_minute >= space*60:
        need = True
    return need

#  取得所有資訊儲存
def get_from_json():
    with open ('information_store.json','r',encoding='utf-8') as f:
        data = f.read()
        data = json.loads(data)
    return data

def get_info_from_json(title:str):
    information_store = get_from_json()
    if title in information_store:
        return information_store[title]
    else:
        return None
    
def store_to_json(data:dict):
    data = json.dumps(data,ensure_ascii=False,indent=4)
    with open ('information_store.json','w',encoding='utf-8') as f:
        f.write(data)
        f.close()

# 取得儲存的資訊
def get_info(key):
    information_store = get_from_json()
    if key in information_store:
        return information_store[key]["info"]
    
def get_from_store():
    with open('store.txt','r',encoding='utf-8') as f:
        text = f.read()
        f.close()
    return text

# 地區對應的 CID 字典
CID_MAPPING = {
    "基隆市": "11017",
    "台北市": "63",
    "臺北市": "63",
    "新北市": "65",
    "桃園市": "68",
    "新竹市": "10018",
    "新竹縣": "10004",
    "苗栗縣": "10005",
    "台中市": "66",
    "彰化縣": "10007",
    "南投縣": "10008",
    "雲林縣": "10009",
    "嘉義市": "10020",
    "嘉義縣": "10010",
    "台南市": "67",
    "高雄市": "64",
    "屏東縣": "10013",
    "宜蘭縣": "10002",
    "花蓮縣": "10015",
    "澎湖縣": "10016",
    "金門縣": "09020",
    "連江縣": "09007"
}

def scrape_table_selenium(cid):
    url = f"https://www.cwa.gov.tw/V8/C/W/County/County.html?CID={cid}"
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)  # 等待 JavaScript 加載完成
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "PC_Week_MOD", "class": "table table-bordered"})
    if not table:
        return []

    rows = table.find_all("tr")
    table_data = []
    for row in rows:
        cells = row.find_all(["td", "th"])
        row_data = []
        for cell in cells:
            celsius_span = cell.find("span", class_="tem-C is-active")
            if celsius_span:
                row_data.append(celsius_span.get_text(strip=True))
            else:
                row_data.append(cell.get_text(strip=True))
        table_data.append(row_data)
    return table_data

def format_weather_output(table_data):
    if not table_data or len(table_data) < 2:
        return "表格資料不足，請稍後再試。"

    location = table_data[0][0]
    dates = table_data[0][1:]
    output = f"{location} - 🌤️ 未來一周天氣預報\n\n"

    for date_idx, date in enumerate(dates):
        output += f"🗓️ {date}\n"
        for row in table_data[1:]:
            label = row[0]
            value = row[date_idx + 1]
            if label == "白天":
                emoji = "☀️"
            elif label == "晚上":
                emoji = "🌙"
            elif label == "體感溫度":
                emoji = "🌡️"
            elif label == "紫外線":
                emoji = "🌞"
            else:
                emoji = ""
            output += f"{emoji} {label}: {value}\n"
        output += "\n"
    return output

def get_weather_forecast(location):
    cid = CID_MAPPING.get(location)
    if not cid:
        return "地區名稱無效，請重新輸入。"

    table_data = scrape_table_selenium(cid)
    if not table_data:
        return "無法取得天氣資料，請稍後再試。"
    return format_weather_output(table_data)