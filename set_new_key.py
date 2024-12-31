import google.generativeai as generativeai
from URL_load import scrape_data
import json
from datetime import datetime
import time
import os
import dotenv
import re

dotenv.load_dotenv()
api_key = os.getenv("gemini_api_key")
generativeai.configure(api_key=api_key)
with open("keyword_url.json", "r", encoding="utf-8") as f:
    key_url_dict = json.load(f)
    key_url_list = list(key_url_dict.keys())

with open("keyword.json", "r", encoding="utf-8") as f:
    key_list = json.load(f)

def check_info(key,info):
    model = generativeai.GenerativeModel("gemini-2.0-flash-exp")
    prompts = f"""Is the information {info} relevant to the {key}.
                  If the information shows that there are relevant information, please reply with 'true'.
                  Else if the information shows that there are not any relevant information, please reply with 'true'.
                  Reply with 'true' or 'false'.
                  Also provide the reason in zh-TW.
                  """
    resp = model.generate_content(prompts)
    return resp.text

def set_new_key(key,url,xpath):
    resp = check_info(key,scrape_data(url,xpath))
    print("judging the information...")
    if re.search("true",resp):
        if key in key_list:
            if key not in key_url_list:
                url_data = [url,xpath]
                key_url_dict[key] = url_data
                url_data = json.dumps(key_url_dict,ensure_ascii=False)
                with open("keyword_url.json", "w", encoding="utf-8") as f:
                    f.write(url_data)
                print(set_info(key))
                return "The keyword has been added successfully."
            else:
                print(set_info(key))
                return "The keyword already exists."
        else:
            key_list.append(key)
            key_url_dict[key] = [url,xpath]
            url_data = json.dumps(key_url_dict,ensure_ascii=False, indent=4)
            with open("keyword_url.json", "w", encoding="utf-8") as f:
                f.write(url_data)
            key_data = json.dumps(key_list,ensure_ascii=False, indent=4)
            with open("keyword.json", "w", encoding="utf-8") as f:
                f.write(key_data)
            print(set_info(key))
            return "The keyword has been added successfully."
    else:
        return "The information is not relevant to the requirements."

def set_info(key):
    with open("information_store.json", "r", encoding="utf-8") as f:
        info_dict = json.load(f)
    url = key_url_dict[key][0]
    xpath = key_url_dict[key][1]
    info = scrape_data(url,xpath)
    t = time.strftime("%Y-%m-%d %H:%M")
    print("judging the information...")
    resp = check_info(key,info)
    print(info)
    print(resp)
    info_dict[key] = {"info": info, "time": t, "space": 0.5}
    print(info_dict)
    info_data = json.dumps(info_dict,ensure_ascii=False, indent=4)
    with open("information_store.json", "w", encoding="utf-8") as f:
        f.write(info_data)
    return "The information has been added successfully."
    