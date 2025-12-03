import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown,display
from openai import OpenAI
load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")
openAi=OpenAI()
system_prompt="You are Majima from Yakuza 0 and speak in his way"
user_prompt="I get bullied what should I do?"
messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}]
response=openAi.chat.completions.create(model="gpt-5-nano",messages=messages)
print(response.choices[0].message.content)