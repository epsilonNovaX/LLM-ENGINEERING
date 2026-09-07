import os
import glob
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
from pathlib import Path

# Basic Setup

load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
MODEL="gpt-4-mini"
openai=OpenAI()
SYSTEM_PREFIX = """
You represent Insurellm, the Insurance Tech company.
You are an expert in answering questions about Insurellm; its employees and its products.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so.

Relevant context:
"""
# Retrieve the documents that are needed in a dictionary (i.e the products and the employees)

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

"""

    1. Get the relevant documentation (in our case the employees data and the products)
    * These are accessed by glob which gives the name of the file and then the name of the file is stored in the dictionary with the required data 
    2. 


"""