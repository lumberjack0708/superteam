import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
endpoint = os.getenv("GPT_endpoint")
key = os.getenv("GPT_Key")
model_name = "gpt-35-turbo"  # Your model name


def get_text(text):
    client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_version="2024-02-01",
    api_key=key
    )

    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": text,  # Your question can go here
            },
        ],
    )

    print(f"return:{completion.choices[0].message.content}")
    return completion.choices[0].message.content
