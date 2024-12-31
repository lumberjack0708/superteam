# Change Log
## [1.0.0] - 2024-12-21
### added
- 新增`Loading_ex.py`，功能為使用者發送訊息時先有loading animation動畫，回覆生成結束之後才會取代動畫輸出結果，為範例程式碼
- 於`gemini.py`新增loading animation功能，用戶發送訊息後會先跳loading動畫，生成結束後輸出結果會將loading結果替換
- 於`vision`中增加loading animation
- 在爬蟲時增加loading animation
### fixed
- 修改`.env.example`參數內容，使其符合目前版本
### changed
- 調整loading animation秒數
- 對`gemini.py`的prompts進行調整
- 於`main.py`更新程式碼片段使其可調用`gemini.py`中的`chat_with_loading`函數
### removed
- 取消`gemini.py`中`chat_with_loading`的time.sleep

## [1.1.0] - 2024-12-21
### added
- 於`cloth.py` 中新增讀取氣溫及降雨機率功能
- 於`cloth.json`增加參數內容

## [1.2.0] - 2024-12-22
### added
- 新增`requirements.txt`
- 於`weather_forecast.py`中新增`get_city`以讀取地址訊息中的城市
### changed
- 更新`main.py`程式碼片段，使其可調用`weather_forecast.py`中的`get_weather_forecast`參數

## [1.2.1] - 2024-12-23
### changed
- 變更爬蟲的間隔時間(1.5hr -> 0.5hr)
### fixed
- 修正了`@氣溫`的xpath問題

## [1.3.0] - 2020-12-26
### added
- 新增了關鍵字`@颱風消息`
- 新增`set_new_key.py`可以使用其中的`set_new_key`新增新的關鍵字

## [1.4.0] - 2020-12-31
### added
- 新增了關鍵字`@空氣品質`

## [1.2.0] - 2024-12-31
### added
- 於`cloth1.py`  中新增讀取氣溫及降雨機率功能
- 於`cloth2.py`  中新增讀取紫外線功能
- 於`cloth.json`增加參數內容