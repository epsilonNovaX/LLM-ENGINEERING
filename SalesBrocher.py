#BASIC IMPORT

from openai import OpenAI
import os
from bs4 import BeautifulSoup
import requests 
from dotenv import load_dotenv

# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
# BASIC SETUP
load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
openai=OpenAI()

