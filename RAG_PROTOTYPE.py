# BASIC IMPORTS
import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import glob

# BASIC SETUP
load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
openai=OpenAI()
MODEL="gpt-4.1-nano"
SYSTEM_PREFIX="""
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
"""

# STORE THE KNOWLEDGE BASE IN A DICTIONARY

knowledge={}

filenames=glob.glob("knowledge-base/employees/*")
for filename in filenames:
    name=Path(filename).stem.split(' ')[-1]
    with open(filename,"r",encoding="utf-8") as f:
        knowledge[name.lower()]=f.read()

filenames=glob.glob("knowledge-base/products/*")
for filename in filenames:
    name=Path(filename).stem
    with open(filename,"r",encoding="utf-8") as f:
        knowledge[name.lower()]=f.read()
# The function that works like RAG 
def get_relevant_context(msg):
    text=''.join(ch for ch in msg if ch.isalpha() or ch.isspace()) # character wise check to remvoe !,? etc 
    words=text.lower().split() # turns into a list 
    relevant_context=[]
    for word in words:
        if word in knowledge:
            relevant_context.append(knowledge[word])
    return relevant_context
# Just a seperate function to check if there is a response
def additional_context(msg):
    pass
# gradio function 
#gradio call 