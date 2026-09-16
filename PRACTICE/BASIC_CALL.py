import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
openai=OpenAI()
MODEL="gpt-4.1-nano"

sys_prompt="You are a helpful assisstant."
message="What is 2+2"
messages=[{"role":"system","content":sys_prompt},{"role":"user","content":message}]

response=openai.chat.completions.create(model=MODEL,messages=message)
print(response.choices[0].message.content)