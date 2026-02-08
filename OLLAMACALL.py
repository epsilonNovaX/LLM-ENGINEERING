import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")
OLLAMA_BASE="http://localhost:11434/v1"
ollamaAI=OpenAI(base_url=OLLAMA_BASE,api_key="DAMEIDANEI")
response=ollamaAI.chat.completions.create(model="llama3.2",messages=[{"role":"user","content":"Tell me a fun fact"}])
print(response.choices[0].message.content)