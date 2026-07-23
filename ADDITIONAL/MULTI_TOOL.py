import os
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")
openai=OpenAI()
MODEL="gpt-5-mini"
sys_prompt="""YOU ARE A HELPFUL ASSISTANT. FOR A FLIGTH APPLICATION KNOWN AS FLIGHTAI
                GIVE SHORT CLEAR ANSWERS, NO MORE THAN ONE SENTENCE. IF YOU DON'T KNOW THE ANSWER JUST SAY SO"""


def chat(msg,history):
    history=[{"role":h["role"],"content":h["content"]}for h in history]
    messages=[{"role":"system","content":sys_prompt}]+history+[{"role":"user","content":msg}]
    response=openai.chat.completions.create(model=MODEL,messages=messages)
    res=""
    for chunck in response:
        res+=chunck.choices[0].delta.content or ""
        yield res
gr.ChatInterface(fn=chat).launch(inbrowser=True)