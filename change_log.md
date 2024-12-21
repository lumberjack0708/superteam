# Change Log

## 2024-xx-xx（範例格式）
### added（新增功能放這邊）
- xxx
### fixed（錯誤修改放這邊）
- xxx


## 2024-12-21
### added
- 新增`Loading_ex.py`，功能為使用者發送訊息時先有loading animation動畫，回覆生成結束之後才會取代動畫輸出結果，為範例程式碼
- 於`gemini.py`新增loading animation功能，用戶發送訊息後會先跳loading動畫，生成結束後輸出結果會將loading結果替換
- 於`main.py`更新程式碼片段使其可調用`gemini.py`中的`chat_with_loading`函數
- 於`vision`中增加loading animation
- 在爬蟲時增加loading animation
### fixed
- 修改`.env.example`參數內容，使其符合目前版本
- 取消`gemini.py`中`chat_with_loading`的time.sleep
- 調整loading animation秒數
- 對gemini的prompts進行調整


 2024-12-21
### added
- 於`cloth.py` 中新增讀取氣溫及降雨機率功能
- 於`cloth.json`增加參數內容


## 2024-12-21
### added
- 創建`weather_forecast.py` 增加抓取一周天氣預報
- 增加`get_weather_forecast`可接收的輸入類型
- 將get_weather_forecast串接至main
### fixed
