import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")
openAI=OpenAI()
response=openAI.chat.completions.create(model="gpt-5-nano",messages=[{"role":"user","content":"Tell me a fun fact"}])
print(response.choices[0].message.content)