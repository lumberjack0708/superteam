from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import re
import matplotlib.pyplot as plt

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
city_list = list(CID_MAPPING.keys())

def scrape_table_selenium(cid):
    url = f"https://www.cwa.gov.tw/V8/C/W/County/County.html?CID={cid}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    time.sleep(3)

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "PC_Week_MOD", "class": "table table-bordered"})
    if not table:
        print("找不到目標表格")
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
        return "表格資料不足"

    location = table_data[0][0]
    dates = table_data[0][1:]
    output = f"{location} - \ud83c\udf24\ufe0f 未來一周天氣預報\n \n"

    for date_idx, date in enumerate(dates):
        output += f"\ud83d\uddd3\ufe0f {date}\n"
        for row in table_data[1:]:
            label = row[0]
            value = row[date_idx + 1]

            if label == "白天":
                emoji = "\u2600\ufe0f"
            elif label == "晚上":
                emoji = "\ud83c\udf19"
            elif label == "體感溫度":
                emoji = "\ud83c\udf21\ufe0f"
            elif label == "紫外線":
                emoji = "\ud83c\udf1e"
            else:
                emoji = ""

            output += f"{emoji} {label}: {value}\n"
        output += "\n"

    return output

def plot_weather_trend(dates, day_temps, night_temps, rain_chances):
    plt.figure(figsize=(10, 6))

    plt.plot(dates, day_temps, label='Day Temp (°C)', marker='o', linestyle='-')
    plt.plot(dates, night_temps, label='Night Temp (°C)', marker='o', linestyle='--')

    plt.bar(dates, rain_chances, alpha=0.5, label='Rain Chance (%)')

    plt.title("Weather Trends for the Next Week")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C) / Rain Chance (%)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    file_path = "/mnt/data/weather_trend.png"
    plt.savefig(file_path)
    plt.close()

    return file_path

def get_weather_forecast(location):
    location = get_city(location)
    cid = CID_MAPPING.get(location)
    if not cid:
        return "地區名稱無效，請重新輸入。"

    table_data = scrape_table_selenium(cid)
    if table_data:
        return format_weather_output(table_data)
    else:
        return "無法取得天氣資料，請稍後再試。"

def get_city(text):
    for city in city_list:
        if re.search(city, text):
            CID = CID_MAPPING[city]
            print(CID)
            text = city
            return text
