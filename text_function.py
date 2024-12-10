import re
import json
import time
from datetime import datetime

with open ('keyword_url.json','r',encoding='utf-8') as f:
    url_dict = f.read()
    url_dict = json.loads(url_dict)

with open ('keyword.json','r',encoding='utf-8') as f:
    url_list = f.read()
    url_list = json.loads(url_list)

# 關鍵詞辨認及回復相關資訊
def main_text(text,predict=False):
    if predict == True:
        return f"使用者的問題:當下天氣狀況;\n預測結果:{text};\n幫我生成簡單回應並給予建議"
    else:
        is_get = False
        for i in range(len(url_list)):
            if re.search(url_list[i],text):
                is_get = True
                result = url_list[i]
                break
        if is_get == True:
            refresh = time_space(get_info_from_json(result))
            if refresh == True:
                res = get_specia_reply(text,result)
                res = cobi_test(text,result,res)
                return res,is_get
            else:
                res = get_info(result)
                res = cobi_test(text,result,res)
                return res,is_get
        else:
            print(f"return message: {text}")
            res = text
            return res,is_get

# 關鍵詞搜索及爬蟲資料儲存   
def get_specia_reply(text,key):
    from spider import get_inf
    url = url_dict[key][0]
    xpath = url_dict[key][1]
    re_inf = get_inf(url,xpath)
    # print(f"已取得資訊{re_inf}")
    information_store = get_from_json()
    information_store[key]["info"] = re_inf
    information_store[key]["time"] = time.strftime("%Y-%m-%d %H:%M")
    store_to_json(information_store)
    return re_inf

def cobi_test(text,key,info):
    return f"使用者的問題:{text};\n以下是目前已知的{key}資訊：\n{info}。\n幫我以一般人類對話的方式回應"

def store(text):
    with open('store.txt','w',encoding='utf-8') as f:
        f.write(text)
        f.close()

# 時間間隔判斷
def time_space(info:dict):
    need = False
    t1 = info["time"]
    space = info["space"]
    time.sleep(1)
    t2 = time.strftime("%Y-%m-%d %H:%M")
    t1 = datetime.strptime(t1, "%Y-%m-%d %H:%M")
    t2 = datetime.strptime(t2, "%Y-%m-%d %H:%M")
    t_diff = t2 - t1
    t_minute = int(t_diff.total_seconds()/60)
    if t_minute >= space*60:
        need = True
    return need

#  取得所有資訊儲存
def get_from_json():
    with open ('information_store.json','r',encoding='utf-8') as f:
        data = f.read()
        data = json.loads(data)
    return data

def get_info_from_json(title:str):
    information_store = get_from_json()
    if title in information_store:
        return information_store[title]
    else:
        return None
    
def store_to_json(data:dict):
    data = json.dumps(data,ensure_ascii=False,indent=4)
    with open ('information_store.json','w',encoding='utf-8') as f:
        f.write(data)
        f.close()

# 取得儲存的資訊
def get_info(key):
    information_store = get_from_json()
    if key in information_store:
        return information_store[key]["info"]
    
def get_from_store():
    with open('store.txt','r',encoding='utf-8') as f:
        text = f.read()
        f.close()
    return text