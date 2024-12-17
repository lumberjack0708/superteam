import json

with open("cloth.json","r",encoding="utf-8") as f:
    cloth_dict = f.read()
    cloth_dict = json.loads(cloth_dict)

with open("information_store.json","r",encoding="utf-8") as f:
    information_dict = f.read()
    information_dict = json.loads(information_dict)


# print(information_dict)

# print(type(information_dict))

print(type(cloth_dict["recommendations"]))
cloth1 = cloth_dict["recommendations"][0]
#字典
print(type(cloth1))
print('-'*50)
cloth = cloth1["clothing"]
for i in range(len(cloth)):
    print(cloth[i])