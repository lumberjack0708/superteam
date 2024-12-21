import json
from datetime import datetime, timedelta

# 載入服裝建議資料
with open("cloth.json", "r", encoding="utf-8") as f:
    cloth_dict = json.load(f)  # 使用 json.load() 來解析 JSON 文件

# 載入氣象資料
with open("information_store.json", "r", encoding="utf-8") as f:
    information_dict = json.load(f)  # 使用 json.load() 來解析 JSON 文件

# 根據氣溫範圍印出服裝建議
for temperature_range, clothing in cloth_dict['cloth'].items():
    print(f"溫度範圍: {temperature_range}")
    print("建議穿著: ", ", ".join(clothing))  # 用逗號拼接服裝建議
    print('-' * 50)  # 分隔線

# 定義要查詢的城市列表（已經加入所有縣市）
json_data = information_dict  # 定義 json_data
cities = [
    "基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣", 
    "臺中市", "彰化縣", "雲林縣", "南投縣", "嘉義市", "嘉義縣", 
    "臺南市", "宜蘭縣", "花蓮縣", "澎湖縣", "連江縣", "金門縣"
]  # 加入所有縣市

# 針對每個城市，查詢氣溫範圍和降雨機率
for city in cities:
    # 獲取該城市的氣溫範圍
    temp_data = json_data["@氣溫"]["info"]
    # 確認該城市是否存在於資料中，並取得其氣溫範圍
    city_temp = temp_data[temp_data.index(city) + 1] if city in temp_data else "No data"
    print(f"{city} 的氣溫範圍: {city_temp}")

    # 獲取該城市的降雨機率
    rain_data = json_data["@降雨機率"]["info"]
    # 確認該城市是否存在於資料中，並取得其降雨機率
    city_rain = rain_data[rain_data.index(city) + 1] if city in rain_data else "No data"
    print(f"{city} 的降雨機率: {city_rain}")

    print('-' * 50)  # 分隔線

# 檢查是否需要更新氣溫資料
last_update = datetime.strptime(json_data["@氣溫"]["time"], "%Y-%m-%d %H:%M")  # 解析最後更新時間
update_interval = timedelta(hours=json_data["@氣溫"]["space"])  # 計算更新間隔時間
now = datetime.now()  # 獲取當前時間

# 如果當前時間與最後更新時間超過了更新間隔，就需要更新資料
if now - last_update >= update_interval:
    print("需要更新氣溫資料")
else:
    print("資料仍然有效")  # 如果資料還是有效的，就不需要更新


# # print(information_dict)
# # print(type(information_dict))

# # print(information_dict)
# # print(type(information_dict))
# print(type(cloth_dict["recommendations"]))
# cloth1 = cloth_dict["recommendations"][0]
# #字典
# print(type(cloth1))
# print('-'*50)
# cloth = cloth1["clothing"]
# for i in range(len(cloth)):
#     print(cloth[i])

cloth = {
    "summer" : ["T-shirt","Shorts","Sandals"],
    "winter" : ["Coat","Sweater","Boots"],
    "spring" : ["T-shirt","Jeans","Sneakers"],
}

cl = cloth["summer"]
t = ""
for i in range(len(cl)):
    print(cl[i])
    t += cl[i] + " "
print('-'*50)
print(t)




