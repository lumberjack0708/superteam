import requests
import json
import os
import dotenv

dotenv.load_dotenv()
# 設定 API 金鑰與 URL
api_key = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')  # 換成你的 API 金鑰
url = f""

# 設定請求的資料
headers = {
    "Content-Type": "application/json"
}

while True:
    user_input = input("請輸入你的問題 (輸入 'exit' 離開): ")
    if user_input.lower() == 'exit':
        print("已退出程序。")
        break

    payload = {
        "contents": [
            {
                "parts": [{"text": user_input}]  # 使用者輸入的問題
            }
        ]
    }

    # 發送 POST 請求
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # 檢查回應
    if response.status_code == 200:
        response_data = response.json()
        try:
            # 嘗試提取回應中的文字內容
            candidates = response_data.get("candidates", [])
            if candidates:
                text_content = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "No 'text' field found.")
                print("回應: ")
                print(text_content)  # 印出 text 的內容
            else:
                print("No candidates found in the response.")
        except (IndexError, KeyError, TypeError):
            print("Unexpected response format.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
