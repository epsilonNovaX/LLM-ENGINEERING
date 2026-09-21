#IMPORTS

from openai import OpenAI
import os
from dotenv import load_dotenv
import numpy as np
import glob # To access the files 
import tiktoken # To count the tokens 
import gradio as gr
from langchain_openai import OpenAIEmbeddings # To create vector embeddings
from langchain_huggingface import HuggingFaceEmbeddings # To create vector embeddings
from langchain_chroma import Chroma # DB to store Vectors
from langchain_text_splitters import RecursiveCharacterTextSplitter # To recursively split the text
from langchain_community.document_loaders import DirectoryLoader, TextLoader 
import plotly.graph_objects as go
from sklearn.manifold import TSNE

# BASIC SETUP
MODEL = "gpt-4.1-nano"
db_name = "vector_db"
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

# COUNTING THE NUMBER OF CHARACTERS AND THUS THE TOTAL TOKEN COUNT

knowledge_base_path="knowledge-base/**/*.md"
files=glob.glob(knowledge_base_path,recursive=True)

print(f"Found {len(files)} files in the knowledge base")

entire_knowledge_base=""

for file in files:
    with open(file,"r",encoding="utf-8") as f:
        entire_knowledge_base+=f.read()
        entire_knowledge_base+="\n\n"

print(f" The total characters in the entire knowledge base:{len(entire_knowledge_base)}")

encoding=tiktoken.encoding_for_model(MODEL)
tokens=encoding.encode(entire_knowledge_base)

token_count = len(tokens)
print(f"Total tokens for {MODEL}: {token_count:,}")


# NOW LOADING THE DOCUMENTS INTO LIST USING LANGCHAINS DIRECTORY LOADERS AND THEN SPILITING THE TEXT

folders=glob.glob("knowledge-base/*")

documents=[]

for folder in folders:
    doc_type=os.path.basename(folder)
    loader=DirectoryLoader(folder,glob="**/*.md",loader_cls=TextLoader,loader_kwargs={'encoding':'utf-8'})
    folder_docs=loader.load()
    for doc in folder_docs:
        doc.metadata["doc_type"]=doc_type
        documents.append(doc)

print(f"Loaded {len(documents)} documents")
documents[1]

text_splitters=RecursiveCharacterTextSplitter(chunks_size=100,chunk_overlap=200)
chunks=text_splitters.split_documents(documents)

print(f"Divided into {len(chunks)} chunks")
print(f"First chunk:\n\n{chunks[0]}")
"""
STEPS:
1. BREAK INTO CHUNKS(TEXT SPLITTERS, LOADERS, GLOB)
2. VECTORIZE(EMBEDDINGS AND CHROMA)
3. RETRIEVE (GRADIO)
* VISUALIZE (PLOTLY)
"""