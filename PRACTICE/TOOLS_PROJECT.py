#Basic imports

import os
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
# Basic setup

load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
openai=OpenAI()
sys_prompt="""
            YOU ARE A HELPFUL ASSISTANT FOR AN AIRPLANE SERVICE KNOWN AS FLIGHT AI.
             MAKE THE RESPONSES SHORT IF YOU DON'T KNOW JUST SAY SO. NO MORE THAN 1 SENTENCE
             """
MODEL="gpt-5-mini"

prices={
    "pakistan":"300$",
    "china":"200$",
    "afghanitan":"100$"
}
def generate_image(destination):
    pass
def generate_voice(destination):
    pass
def get_ticket_price(destination):
    print(f"Function called for {destination}")
    price=prices.get(destination.lower(),"unknown location")
    image=generate_image(destination)
    voice=generate_voice(destination)
    return price
# The passable JSON to Tool call
price_function={
    "name":"get_ticket_price",
    "description":"The function that returns the price for destination",
    "parameters":{
        "type":"object",
        "properties":{
            "destination":{
                "type":"string",
                "description":"The destination for which price is required"
            },
        },
        "required":["destination"]
    }
}
tools=[{"type":"fucntion","function":price_function}]

def handle_tool_calls(msg):
    pass

def chat(msg,history):
    pass

gr.ChatInterface(fn=chat).launch(inbrowser=True)