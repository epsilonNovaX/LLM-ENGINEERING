import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from IPython.display import display, Markdown
import requests
from urllib.parse import urljoin
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
#5. Get the text from the scrape'
#6. return the title and text'

def fetch_website_links(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    links = []

    for link in soup.find_all("a", href=True):
        href = link["href"]

        # Convert relative URLs to absolute URLs
        absolute_url = urljoin(url, href)

        links.append(absolute_url)

    # Remove duplicates while preserving order
    unique_links = list(dict.fromkeys(links))

    return unique_links

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

link_sys_prompt="""
    You are provided with a list of links found on a webpage. 
    You are able to decide which of the links woul dbe most relevant to include in a brochure for a product. 
    Such as links to an About page, or a Company page, or a Careers/Jobs pages.
    You should respond in JSON format like following:
    {
        "links":[
            {"type":"about page","url":"https://example.com/about"},
            {"type":"careers page","url":"https://example.com/careers"}
        ]
    }
"""

def get_links_user_prompt(url):
    user_prompt=f"""
        HERE ARE THE LIST OF LINKS ON THE WEBSITER {url}-
        please decide which of the links are relevant for a brochure about the company,
        respond with full https URL in json format.
        Do not include terms of service, Privacy, email links. 
        Links (some might be relative links):


    """
    links=fetch_website_links(url)
    user_prompt+="\n".join(links)
    return user_prompt
print(get_links_user_prompt("https://cnn.com"))