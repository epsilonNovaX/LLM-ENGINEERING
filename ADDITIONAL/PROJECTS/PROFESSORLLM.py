import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich.console import Console
from rich.markdown import Markdown

console = Console()
load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
system_message="""You are an expert university professor.

Your goal is to teach the content clearly and accurately.

Always use Markdown formatting with headings, subheadings, bullet points, numbered lists, and tables when appropriate.

Explain difficult ideas simply before introducing technical terms.

Give practical examples and analogies.

Assume the student is learning the topic for the first time."""
user_message_prefix="""
Turn the following webpage into professional lecture notes.

Use this exact structure:

# Lecture Title

## Overview
- Brief summary

## Learning Objectives
- Objective 1
- Objective 2
- Objective 3

## Key Concepts
Explain each concept using headings and bullet points.

## Examples
Give practical real-world examples.

## Important Definitions
Create a table with:
| Term | Definition |

## Key Takeaways
Summarize the most important points.

## Quiz
Create:
- 5 multiple-choice questions
- 5 short-answer questions

## Answers
Provide the answers at the end.

Webpage:
"""
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
response=summarize("https://cnn.com")
console.print(Markdown(response))