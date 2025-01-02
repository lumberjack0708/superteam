import json


with open('information_store.json', "r", encoding="utf-8") as f:
    data =f.read()
    data = json.loads(data)
print(data['@空氣品質']['info'])
with open('cloth.json', "r", encoding="utf-8") as f:
    clothdata =f.read()
    clothdata = json.loads(clothdata)
cloth = f"{clothdata['air_quality']},{clothdata['ranges']}"
print("-"*50)
print(cloth)