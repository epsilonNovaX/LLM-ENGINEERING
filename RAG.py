# BASIC IMPORTS
import os
from openai import OpenAI
from dotenv import load_dotenv
import glob
import gradio as gr
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
#from langchain_community.document_loaders import DirectoryLoader, TextLoader
#from langchain_text_splitters import RecursiveCharacterTextSplitter
#from sklearn.manifold import TSNE
#import plotly.graph_objects as go

# Basic Setup
MODEL = "gpt-4.1-nano"
db_name = "vector_db"
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
#Get the total characters 

entireKnowledgeBase=""
knowledgeBasePath="knowledge-base/**/*.md"
files=glob.glob(knowledgeBasePath,recursive=True)
print(f"Found {len(files)} files in the knowledge base")
for filePath in files:
    with open(filePath,"r",encoding="utf-8") as f:
        entireKnowledgeBase+=f.read()
        entireKnowledgeBase+='\n'
print(f"Total characters in knowledge base: {len(entireKnowledgeBase):,}")



"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
STEPS:
1. Divide the documents into chunks

i. Got the total characters in the total knowledge base 




2. Vectorize the chunks
3. Retrieve data as needed


------------------------------------------------------------------------------------------------------------------------------------------





XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""