from selenium import webdriver
import time
from bs4 import BeautifulSoup

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
    # 建立目標 URL
    url = f"https://www.cwa.gov.tw/V8/C/W/County/County.html?CID={cid}"

    # 建立 WebDriver
    driver = webdriver.Chrome()
    driver.get(url)

    # 等待 JavaScript 加載完成
    time.sleep(3)

    # 取得完整的 HTML
    html = driver.page_source
    driver.quit()

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "PC_Week_MOD", "class": "table table-bordered"})
    if not table:
        print("找不到目標表格")
        return []

    rows = table.find_all("tr")

    # 解析表格
    table_data = []
    for row in rows:
        cells = row.find_all(["td", "th"])
        row_data = []
        for cell in cells:
            # 優先抓取 class="tem-C is-active" 的攝氏溫度
            celsius_span = cell.find("span", class_="tem-C is-active")
            if celsius_span:
                row_data.append(celsius_span.get_text(strip=True))
            else:
                row_data.append(cell.get_text(strip=True))
        table_data.append(row_data)

    return table_data

def format_weather_output(table_data):
    # 格式化輸出資料
    if not table_data or len(table_data) < 2:
        return "表格資料不足"

    # 第一列為標題
    location = table_data[0][0]  # 地名
    dates = table_data[0][1:]    # 日期
    output = f"{location} - 🌤️ 未來一周天氣預報\n \n"

    # 每列數據
    for date_idx, date in enumerate(dates):
        output += f"🗓️ {date}\n"  # 僅顯示一次日期
        for row in table_data[1:]:
            label = row[0]  # 例如 "白天", "晚上", "體感溫度", "紫外線"
            value = row[date_idx + 1]  # 對應當前日期的數值

            # 根據標籤添加對應的表情符號
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
        output += "\n"  # 每個日期之間空一行

    return output

def get_weather_forecast(location):
    # 根據地區名稱取得天氣預報
    cid = CID_MAPPING.get(location)
    if not cid:
        return "地區名稱無效，請重新輸入。"

    table_data = scrape_table_selenium(cid)
    if table_data:
        return format_weather_output(table_data)
    else:
        return "無法取得天氣資料，請稍後再試。"
