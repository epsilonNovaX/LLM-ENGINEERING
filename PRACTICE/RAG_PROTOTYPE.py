#Basic imports
import os
from openai import OpenAI
from dotenv import load_dotenv
import glob
from pathlib import Path
# Basic setup
load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
openai=OpenAI()
SYSTEM_PREFIX = """
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
"""
#The dict that will contain all the knowledge about products and employees

knowledge={}
# Loading all the files

files=glob.glob("knowledge-base/employees/*")
for file in files:
    name=Path(file).stem.split(' ')[-1]
    with open(file,"r",encoding="utf-8") as f:
        knowledge[name.lower()]=f.read()

files=glob.glob("knowledge-base/products/*")
for file in files:
    name=Path(file).stem
    with open(file,"r",encoding="utf-8") as f:
        knowledge[name.lower()]=f.read()
print(knowledge)