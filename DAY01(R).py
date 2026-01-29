import os
from openai import OpenAI
from IPython.display import Markdown,display
import requests
from dotenv import load_dotenv
load_dotenv(override=True)
api_key=os.getenv('OPENAI_API_KEY')
ObjAI=OpenAI()
sysPrompt="""YOU ARE NISHIKIYAMA FROM YAKUZA KIWAMI. """
usPrompt="""How can I be like you???"""
messages=[{"role":"system","content":sysPrompt},{"role":"user","content":usPrompt}]
response=ObjAI.chat.completions.create(model="gpt-5-nano",messages=messages)
print(response.choices[0].message.content)