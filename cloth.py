import json

with open("cloth.json","r",encoding="utf-8") as f:
    cloth_dict = f.read()
    cloth_dict = json.loads(cloth_dict)

with open("information_store.json","r",encoding="utf-8") as f:
    information_dict = f.read()
    information_dict = json.loads(information_dict)

for temperature_range, clothing in cloth_dict['cloth'].items():
    print(f"溫度範圍: {temperature_range}")
    print("建議穿著: ", ", ".join(clothing))
    print('-' * 50)


json_data = information_dict  # 定義 json_data
data = json_data["@氣溫"]["info"]
keelung_temp = data[data.index("基隆市") + 1]  # 獲取基隆市的氣溫範圍
print(keelung_temp)  # 輸出：16~16

data = json_data["@降雨機率"]["info"]
taipei_rain = data[data.index("臺北市") + 1]  # 獲取臺北市的降雨機率
print(taipei_rain)  # 輸出：30%


from datetime import datetime, timedelta

last_update = datetime.strptime(json_data["@氣溫"]["time"], "%Y-%m-%d %H:%M")
update_interval = timedelta(hours=json_data["@氣溫"]["space"])
now = datetime.now()

if now - last_update >= update_interval:
    print("需要更新氣溫資料")
else:
    print("資料仍然有效")

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




