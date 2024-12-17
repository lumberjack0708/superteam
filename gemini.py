import google.generativeai as generativeai
import os

api_key = os.getenv("gemini_api_key")
generativeai.configure(api_key=api_key)
text = "生命的意義是甚麼？"
response = generativeai.GenerativeModel("gemini-2.0-flash-exp").generate_content(text)
print(response.text)