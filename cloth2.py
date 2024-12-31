import json
import random

def read_and_combine_data():
    # 載入服裝建議資料
    with open("cloth.json", "r", encoding="utf-8") as f:
        cloth_dict = json.load(f)  # 使用 json.load() 來解析 JSON 文件

    # 載入氣象資料
    with open("information_store.json", "r", encoding="utf-8") as f:
        information_dict = json.load(f)  # 使用 json.load() 來解析 JSON 文件

    # 定義要查詢的城市列表（已經加入所有縣市）
    cities = [
        "基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣", 
        "臺中市", "彰化縣", "雲林縣", "南投縣", "嘉義市", "嘉義縣", 
        "臺南市", "宜蘭縣", "花蓮縣", "澎湖縣", "連江縣", "金門縣"
    ]  # 加入所有縣市

    results = []

    # 針對每個城市，查詢氣溫範圍和降雨機率
    for city in cities:
        # 獲取該城市的氣溫範圍
        temp_data = information_dict["@氣溫"]["info"]
        city_temp = temp_data[temp_data.index(city) + 1] if city in temp_data else "No data"

        # 確保 city_temp 是有效的數字範圍
        if city_temp != "No data" and '~' in city_temp:
            city_temp_min = int(city_temp.split('~')[0])
        else:
            city_temp_min = None

        # 根據氣溫範圍隨機挑選幾個服裝建議
        clothing_suggestion = "No suggestion"
        if city_temp_min is not None:
            for temperature_range, clothing in cloth_dict['cloth'].items():
                if '~' in temperature_range:
                    temp_range_min, temp_range_max = map(int, temperature_range.split('~'))
                    if temp_range_min <= city_temp_min <= temp_range_max:
                        clothing_suggestion = ", ".join(random.sample(clothing, min(3, len(clothing))))
                        break
                elif '>=' in temperature_range:
                    temp_range_min = int(temperature_range.split('>=')[1])
                    if city_temp_min >= temp_range_min:
                        clothing_suggestion = ", ".join(random.sample(clothing, min(3, len(clothing))))
                        break

        # 串連成句子
        result = f"{city} 的氣溫範圍是 {city_temp}，建議穿著: {clothing_suggestion}。"
        results.append(result)

    return results

# 調用函數並打印結果
combined_data = read_and_combine_data()
for data in combined_data:
    print(data)