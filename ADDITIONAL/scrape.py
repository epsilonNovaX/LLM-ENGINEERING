import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup
load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
system_message="""Summarize pages in a funny way"""
user_message_prefix="""Summarize the content I have provided"""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}
#1. Reuquest content
#2. scrape contetn using beautilfulSoup
#3. get title
#4. remove irrelevant (as non saphisticated)
#5. Get the text from the scrape
#6. return the title and text
def fetch_website_content(url):
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,"html.parser")
    title=soup.title.string if soup.title else "No title found"
    for irrelevant in soup.body(["script","style","img","input"]):
        irrelevant.decompose()
    text=soup.body.get_text(separator="\n",strip=True)
    return title+"\n\n"+text
def messages_for(website):
    return [
        {"role":"system","content":system_message},
        {"role":"user","content":user_message_prefix+website}
    ]
openai=OpenAI()
def summarize(url):
    website=fetch_website_content(url)
    res=openai.chat.completions.create(model="gpt-5-mini",messages=messages_for(website))
    return res.choices[0].message.content
print(summarize("https://cnn.com"))