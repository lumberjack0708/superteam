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




