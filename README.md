# superteam
# Weather Assistant Line Bot

一個基於 LINE Messaging API 和 Google Gemini AI 開發的天氣助手聊天機器人，提供即時天氣資訊、天氣預報和穿搭建議。

## 功能特點

- 即時天氣資訊查詢
- 未來一週天氣預報
- 颱風資訊查詢
- 根據溫度和降雨機率提供穿搭建議
- 支援圖片識別天氣狀況
- 智慧對話功能（基於 Google Gemini AI）
- 動態載入動畫提升使用體驗
- 未來一週農業天氣預報與農務建議

## 系統需求

- Python 3.8+
- LINE Messaging API 帳號
- Google Gemini API 金鑰
- Chrome WebDriver (用於爬蟲功能)

## 安裝步驟

1. 克隆專案：
```bash
git clone https://github.com/yourusername/weather-assistant-linebot.git
```

2. 安裝相依套件：
```bash
pip install -r requirements.txt
```

3. 設定環境變數：
- 複製 .env.example 為 .env
- 填入以下資訊：
    - LINE_CHANNEL_ACCESS_TOKEN
    - LINE_CHANNEL_SECRET
    - Ngrok_url
    - gemini_api_key


## 使用方法

### 啟動Line Bot：
```bash
python main.py
```
### LINE Bot 指令：
- `@天氣`：上傳天氣圖片進行分析
- `@天氣預報`：查詢指定地區的天氣預報
- `@氣溫`：查詢即時氣溫資訊
- `@降雨機率`：查詢降雨機率
- `@颱風消息`：颱風資訊查詢
- `@空氣品質`：空氣品質資訊查詢
- `@服裝建議`：根據地點給出服裝建議
- `@農情資訊`：根據地點給出農業相關建議

## 專案架構
```
superteam/
├── main.py               # 主程式進入點
├── gemini.py             # Google Gemini AI 整合
├── weather_forecast.py   # 天氣預報功能
├── vision.py             # 圖片識別功能
├── cloth.py              # 穿搭建議功能
├── text_function.py      # 文字處理功能
├── URL_load.py           # 網頁爬蟲功能
├── requirements.txt      # 相依套件清單
├── .env.example          # 環境變數範例
└── farm.py               # 農情資訊功能
```
## 版本更新
詳細更新資訊請參考 [change_log.md](change_log.md)。

## 授權資訊
本專案採用 MIT 授權。

## 貢獻指南
歡迎提交 Issue 和 Pull Request 來協助改善專案。

## 開發團隊:superteam
- 開發者:**李宇涵**、陳廷鈞、孫葦傑、葉子羽、張子頡

## 致謝
- LINE Messaging API
- Google Gemini AI
- 中央氣象署


