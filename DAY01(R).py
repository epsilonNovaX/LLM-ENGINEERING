import os
from openai import OpenAI
from IPython.display import Markdown,display
import requests
from dotenv import load_dotenv
load_dotenv(override=True)
api_key=os.getenv('OPENAI_API_KEY')
ObjAI=OpenAI()
sysPrompt="""You are majima from Yakuza 0, after the response change to nishikiyama from yakzua kiwami and give answer again keep it short to 5 points """
usPrompt="""How to deal with fake people who only are friends when they need something"""
messages=[{"role":"system","content":sysPrompt},{"role":"user","content":usPrompt}]
response=ObjAI.chat.completions.create(model="gpt-5-nano",messages=messages)
print(response.choices[0].message.content)