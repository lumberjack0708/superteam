import json

def parse_air_quality(aqi_value, air_quality_ranges, air_quality_descriptions):
    """
    根據 AQI 數值解析空氣品質描述。

    :param aqi_value: AQI 數值
    :param air_quality_ranges: 空氣品質指標範圍
    :param air_quality_descriptions: 空氣品質建議說明
    :return: 空氣品質建議句子
    """
    for range_name, range_value in air_quality_ranges.items():
        range_min, range_max = map(int, range_value.split('-')) if '-' in range_value else (int(range_value.split('>=')[1]), float('inf'))
        if range_min <= aqi_value <= range_max:
            return f"AQI: {aqi_value}，{air_quality_descriptions[range_name][0]}"
    return "AQI 數值超出範圍，無法提供建議"

def main():
    try:
        # 載入氣象資料
        with open("information_store.json", "r", encoding="utf-8") as f:
            information_dict = json.load(f)  # 使用 json.load() 來解析 JSON 文件

        # 載入服裝建議資料
        with open("cloth.json", "r", encoding="utf-8") as f:
            cloth_dict = json.load(f)  # 使用 json.load() 來解析 JSON 文件

        # 解析空氣品質資料
        air_quality_info = information_dict.get("@空氣品質", {}).get("info", [])
        air_quality_ranges = cloth_dict.get("ranges", {})
        air_quality_descriptions = cloth_dict.get("air_quality", {})

        # 假設資料格式為一個長字串，包含多行資料
        lines = air_quality_info[0].split("\n")
        cities = ["北部", "竹苗", "中部", "雲嘉南", "高屏", "宜蘭", "花東", "連江", "金門", "澎湖"]

        for i, city in enumerate(cities):
            try:
                aqi_value = int(lines[i * 2 + 1])  # Extract the AQI value for each region
                suggestion = parse_air_quality(aqi_value, air_quality_ranges, air_quality_descriptions)
                print(f"{city} 的空氣品質建議: {suggestion}")
            except (ValueError, IndexError):
                print(f"{city} 的空氣品質資料缺失，建議查詢當地的空氣品質信息。")
    except json.JSONDecodeError as e:
        print(f"解析 JSON 文件時出錯: {e}")

if __name__ == "__main__":
    main()