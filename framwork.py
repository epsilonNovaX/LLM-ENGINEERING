import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown,display
from openai import OpenAI
from litellm import completion
tell_me_joke=[
    {"role":"user","content":"Tell me a joke"}
]
response=completion(model="openai/gpt-4.1",messages=tell_me_joke)
reply=response.choices[0].message.content
print(reply)