import google.generativeai as generativeai
import os

# Set the API key
api_key = os.getenv("gemini_api_key")
generativeai.configure(api_key=api_key)
response = generativeai.GenerativeModel("gemini-2.0-flash-exp").generate_content("生命的意義是甚麼？")
print(response.text)