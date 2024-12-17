import google.generativeai as generativeai

generativeai.configure(api_key="AIzaSyA_sNkkcQFPrZAWCxJwGWl2ji3f8uiATg8")
response = generativeai.GenerativeModel("gemini-2.0-flash-exp").generate_content("生命的意義是甚麼？")
print(response.text)