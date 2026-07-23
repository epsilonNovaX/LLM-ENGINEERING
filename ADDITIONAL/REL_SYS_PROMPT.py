import os
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr

load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")

openai=OpenAI()
system_prompt="You are a helpful assisstant"
def chat(msg,history):
   history=[{"role":h["role"],"content":h["content"]} for h in history]
   rel_sys_prompt=system_prompt
   if 'yakuza' in msg.lower():
      rel_sys_prompt+="If the yakuza is included, start talking in japanese and sing a random line from bakamitai"
   messages= [{"role": "system", "content": rel_sys_prompt}]+ history+ [{"role": "user", "content": msg}]
   response=openai.chat.completions.create(model="gpt-5-mini",messages=messages,stream=True)
   result=""
   for chunk in response:
      result+=chunk.choices[0].delta.content or ""
      yield result

gr.ChatInterface(fn=chat).launch(inbrowser=True)