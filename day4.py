import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

openai = OpenAI()

messages = [
    {"role": "system", "content": "You are a helpful assistant!"},
    {"role": "user", "content": "Hi! I am Ahmad"},
     {"role": "assistant", "content": "Hello Yakuza Ahmad!"},
    {"role": "user", "content": "What is my name"},
]

response = openai.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages
)

print(response.choices[0].message.content)