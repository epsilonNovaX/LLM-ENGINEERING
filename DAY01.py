import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown,display
from openai import OpenAI
load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")
if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")
openai_client=OpenAI()
message="Hello this is my first message"
messages=[{"role":"user","content":message}]
response=openai_client.chat.completions.create(model="gpt-5-nano",messages=messages)
print(response.choices[0].message.content)