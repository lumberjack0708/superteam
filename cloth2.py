import json
import random

def read_and_combine_data():
    # 載入服裝建議資料
    with open("cloth.json", "r", encoding="utf-8") as f:
        cloth_dict = json.load(f)

    # 載入氣象資料
    with open("information_store.json", "r", encoding="utf-8") as f:
        information_dict = json.load(f)

    # 定義城市列表
    cities = [
        "基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣",
        "臺中市", "彰化縣", "雲林縣", "南投縣", "嘉義市", "嘉義縣",
        "臺南市", "宜蘭縣", "花蓮縣", "澎湖縣", "連江縣", "金門縣"
    ]

    results = []

    for city in cities:
        # 取得氣溫資料
        temp_data = information_dict.get("@氣溫", {}).get("info", [])
        city_temp = "No data"
        if city in temp_data:
            index = temp_data.index(city) + 1
            if index < len(temp_data):
                city_temp = temp_data[index]

        # 取得降雨機率資料
        rain_data = information_dict.get("@降雨機率", {}).get("info", [])
        city_rain = "No data"
        if city in rain_data:
            index = rain_data.index(city) + 1
            if index < len(rain_data):
                city_rain = rain_data[index]

        # 解析氣溫
        city_temp_min = None
        if city_temp != "No data":
            try:
                separator = '~' if '~' in city_temp else '-'
                city_temp_min = int(city_temp.split(separator)[0])
            except (ValueError, AttributeError):
                pass

        # 根據氣溫隨機挑選建議
        clothing_suggestion = "No suggestion"
        if city_temp_min is not None:
            for temperature_range, clothing in cloth_dict['cloth'].items():
                try:
                    if '~' in temperature_range or '-' in temperature_range:
                        separator = '~' if '~' in temperature_range else '-'
                        temp_range_min, temp_range_max = map(int, temperature_range.split(separator))
                        if temp_range_min <= city_temp_min <= temp_range_max:
                            clothing_suggestion = ", ".join(random.sample(clothing, min(3, len(clothing))))
                            break
                    elif '>=' in temperature_range:
                        temp_range_min = int(temperature_range.split('>=')[1])
                        if city_temp_min >= temp_range_min:
                            clothing_suggestion = ", ".join(random.sample(clothing, min(3, len(clothing))))
                            break
                except ValueError:
                    continue

        # 根據降雨機率提供建議
        rain_suggestion = "No suggestion"
        if city_rain != "No data" and '%' in city_rain:
            try:
                rain_percentage = int(city_rain.replace('%', '').strip())
                for rain_range, suggestion in cloth_dict['rain'].items():
                    try:
                        if '-' in rain_range:
                            rain_range_min, rain_range_max = map(int, rain_range.replace('%', '').split('-'))
                            if rain_range_min <= rain_percentage <= rain_range_max:
                                rain_suggestion = suggestion
                                break
                        elif '>=' in rain_range:
                            rain_range_min = int(rain_range.split('>=')[1].replace('%', ''))
                            if rain_percentage >= rain_range_min:
                                rain_suggestion = suggestion
                                break
                    except ValueError:
                        continue
            except ValueError:
                pass

        # 整合輸出結果
        result = f"{city} 的氣溫範圍是 {city_temp}，降雨機率是 {city_rain}，建議穿著: {clothing_suggestion}，降雨建議: {rain_suggestion}。"
        results.append(result)

    return results

# 執行程式並輸出結果
if __name__ == "__main__":
    combined_data = read_and_combine_data()
    for data in combined_data:
        print(data)
