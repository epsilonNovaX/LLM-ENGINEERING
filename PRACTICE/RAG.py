#Basic imports 
from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import glob
import gradio as gr
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader,DirectoryLoader
import tiktoken
import numpy as np

#Basic setup
load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
openai=OpenAI()
db_name="vector_db"
MODEL="gpt-4.1-nano"

# Get the total characters
knowledge_base_path="knowledge-base/**/*.md"
files=glob.glob(knowledge_base_path,recursive=True)
entire_knowledge_base=""
for file in files:
    with open(file,"r",encoding="utf-8") as f:
        entire_knowledge_base+=f.read()
        entire_knowledge_base+="\n\n"
print(f" Total characters : {len(entire_knowledge_base)}")

encoding=tiktoken.encoding_for_model(MODEL)
tokens=encoding.encode(entire_knowledge_base)
token_count=len(tokens)

print(f" The tokens for MODEL {MODEL} : {token_count}")
# now to laod the documetns and make it ready to be divided into chunks

documents=[]

folders=glob.glob("knowledge-base/*")

for folder in folders:
    doc_type=os.path.name(folder)
    loader=DirectoryLoader(folder,glob="**/*.md",loader_cls=TextLoader,loader_kwargs={"encoding":"utf-8"})
    folder_docs=loader.load()
    for doc in folder_docs:
        doc.metadata["doc_type"]=doc_type
        documents.append(doc)


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

print(f"Divided into {len(chunks)} chunks")
print(f"First chunk:\n\n{chunks[0]}")