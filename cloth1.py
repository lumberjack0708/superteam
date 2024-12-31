import json

def read_data(file_path):
    """
    讀取 JSON 文件並返回解析後的數據。

    :param file_path: JSON 文件的路徑
    :return: 解析後的數據
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
        return None
    except json.JSONDecodeError as e:
        print(f"解析 JSON 文件時出錯: {e}")
        return None

def parse_air_quality(aqi_value, air_quality_ranges, air_quality_descriptions):
    """
    根據 AQI 數值解析空氣品質描述。

    :param aqi_value: AQI 數值
    :param air_quality_ranges: 空氣品質指標範圍
    :param air_quality_descriptions: 空氣品質建議說明
    :return: 空氣品質建議句子
    """
    if aqi_value is None:
        return "無法提供建議，因為 AQI 數值缺失。"

    for range_name, range_value in air_quality_ranges.items():
        range_min, range_max = map(int, range_value.split('-')) if '-' in range_value else (int(range_value.split('>=')[1]), float('inf'))
        if range_min <= aqi_value <= range_max:
            return f"AQI: {aqi_value}，{air_quality_descriptions[range_name][0]}"
    return f"AQI: {aqi_value}，數值未涵蓋於範圍內，請參考當地建議。"

def extract_aqi_values(lines, cities):
    """
    提取 AQI 值並按城市返回。

    :param lines: 整理後的空氣品質數據行
    :param cities: 城市列表
    :return: 城市對應的 AQI 值列表
    """
    aqi_values = []
    try:
        # 找到"空品區"的索引，從該位置提取數據
        start_index = lines.index("空品區") + 1
        city_names = lines[start_index:start_index + len(cities)]
        aqi_start_index = start_index + len(cities)
        aqi_values_raw = lines[aqi_start_index:aqi_start_index + len(cities)]

        for city in cities:
            if city in city_names:
                city_index = city_names.index(city)
                try:
                    # 提取數值，過濾非數字內容
                    raw_value = aqi_values_raw[city_index]
                    aqi_value = int(''.join(filter(str.isdigit, raw_value.split()[0])))
                    aqi_values.append(aqi_value)
                except (ValueError, IndexError):
                    print(f"無法解析 {city} 的 AQI 數值，跳過。")
                    aqi_values.append(None)
            else:
                print(f"{city} 的資料缺失。")
                aqi_values.append(None)
    except Exception as e:
        print(f"提取 AQI 資料出錯: {e}")
    return aqi_values

def combine_air_quality_sentences(air_quality_info, air_quality_ranges, air_quality_descriptions, cities):
    """
    生成每個城市的空氣品質建議句子。

    :param air_quality_info: @空氣品質的 info 數據
    :param air_quality_ranges: 空氣品質指標範圍
    :param air_quality_descriptions: 空氣品質建議說明
    :param cities: 城市列表
    :return: 每個城市的建議句子列表
    """
    lines = air_quality_info[0].split("\n")
    aqi_values = extract_aqi_values(lines, cities)
    sentences = []

    for city, aqi_value in zip(cities, aqi_values):
        suggestion = parse_air_quality(aqi_value, air_quality_ranges, air_quality_descriptions)
        sentences.append(f"{city} 的空氣品質建議: {suggestion}")

    return sentences

def main():
    # 載入資料
    information_data = read_data("information_store.json")
    cloth_data = read_data("cloth.json")

    if information_data is None or cloth_data is None:
        print("資料載入失敗，無法繼續執行。")
        return

    air_quality_ranges = cloth_data["ranges"]
    air_quality_descriptions = cloth_data["air_quality"]
    air_quality_info = information_data["@空氣品質"]["info"]

    cities = ["北部", "竹苗", "中部", "雲嘉南", "高屏", "宜蘭", "花東", "連江", "金門", "澎湖"]

    # 合成建議句子
    sentences = combine_air_quality_sentences(air_quality_info, air_quality_ranges, air_quality_descriptions, cities)

    for sentence in sentences:
        print(sentence)

if __name__ == "__main__":
    main()
