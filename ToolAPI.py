#BASIC IMPORTS
import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import gradio as gr

# BASIC SETUPS

load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")

sys_prompt=""