import gradio as gr
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")

openai=OpenAI()
sys_prompt="You are a helpful assistant"
def messages_gpt(prompt):
    messages=[{"role":"system","content":sys_prompt},{"role":"user","content":prompt}]
    res=openai.chat.completions.create(model="gpt-5-mini",messages=messages,stream=True)
    result=""
    for chunk in res:
        result+=chunk.choices[0].delta.content or ""
        yield result
def stream_model(prompt,model):
    if model=="GPT":
       result= messages_gpt(prompt)
    else:
        raise ValueError("Error")
    yield from result
def hello(name):
    return "hello "+name+" !";
msg_input=gr.Textbox(label="Input",info="Enter message",lines=7)
model_selector=gr.Dropdown(["GPT","Ollama"],label="Select Model:")
msg_output=gr.Markdown(label="Output")
demo=gr.Interface(fn=stream_model,title="GPT",inputs=[msg_input,model_selector],outputs=[msg_output],examples=[["Explain transformers","GPT"],["Explain tokens briefly","Ollama"]],flagging_mode="never")
demo.launch(inbrowser=True)

