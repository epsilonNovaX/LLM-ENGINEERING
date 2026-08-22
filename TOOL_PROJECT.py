#BASIC IMPORTS
import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import gradio as gr
import base64
# BASIC SETUPS

load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")
openai=OpenAI()
sys_prompt=""
MODEL="gpt-5-mini"
modelVoice="gpt-audio-1.5"
modelImage="gpt-image-2"