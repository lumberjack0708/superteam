import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 我把儲存檔案的都丟在text_function.py 的store_to_json
# 爬到的會存在information_store.json
def load_json(file_path):
    """讀取 JSON 檔案"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(data, file_path):
    """將資料儲存至 JSON 檔案"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"結果已儲存至 {file_path}")

def scrape_data(url, xpath):
    """使用 Selenium 爬取指定 URL 和 XPath 的內容"""
    print(f"正在爬取 {url} ...")
    results = []

    # 設定 Chrome 選項（無頭模式）
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # 啟動 Selenium 瀏覽器
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)  # 訪問網址
        driver.implicitly_wait(10)  # 等待加載完成

        # 抓取所有符合 XPath 的元素
        elements = driver.find_elements(By.XPATH, xpath)
        for elem in elements:
            results.append(elem.text.strip())

        print(f"成功爬取 {len(results)} 筆資料")
    except Exception as e:
        print(f"爬取失敗: {e}")
    finally:
        driver.quit()  # 關閉瀏覽器

    return results

def main():
    # 讀取 keyword_url.json
    input_file = "keyword_url.json"
    output_file = "output.json"
    data = load_json(input_file)
    output_data = {}

    # 逐項目爬取資料
    for key, value in data.items():
        url, xpath = value[0], value[1]
        output_data[key] = scrape_data(url, xpath)

    # 儲存結果至 output.json
    save_json(output_data, output_file)


