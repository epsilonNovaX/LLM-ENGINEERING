import os
from dotenv import load_dotenv
import requests
import json
from bs4 import BeautifulSoup
from openai import OpenAI
headers = {"Content-Type": "application/json"}
def fetch_website_links(url):
    response=requests.get(url,headers=headers)    
    soup=BeautifulSoup(response.content,"html.parser")
    links=[link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]

print("hello")
load_dotenv(override=True)
api_key=os.getenv('OPENAI_API_KEY')



MODEL='gpt-5-nano'
openai=OpenAI()
links=fetch_website_links("https://edwarddonner.com")
print(links)