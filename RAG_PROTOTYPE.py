#IMPORTS

from openai import OpenAI
import os
from dotenv import load_dotenv
import numpy as np
import glob # To get the path for the file
from pathlib import Path # To get the file name and later split it to store in the dictionary of data
import gradio as gr

# BASIC SETUP
openai=OpenAI()
MODEL = "gpt-4.1-nano"
db_name = "vector_db"
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
SYSTEM_PREFIX = """
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
"""
# LOADING ALL THE EMPLOYEES PART INTO A DICTIONARY

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

# print(knowledge.keys())

# Get what might be relevant in a text

def get_relevant_context(message):
    text = ''.join(ch for ch in message if ch.isalpha() or ch.isspace())
    words=text.lower().split()
    relevant_context=[]
    for word in words:
        if word in knowledge:
            relevant_context.append(knowledge[word])
    return relevant_context
def additional_context(message):
    relevant_context = get_relevant_context(message)
    if not relevant_context:
        result = "There is no additional context relevant to the user's question."
    else:
        result = "The following additional context might be relevant in answering the user's question:\n\n"
        result += "\n\n".join(relevant_context)
    return result
def chat(message, history):
    system_message = SYSTEM_PREFIX + additional_context(message)
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content
view = gr.ChatInterface(chat, type="messages").launch(inbrowser=True)
"""
STEPS:
1. GET ALL THE DATABASE IN A DICTIONARY
2. 
"""