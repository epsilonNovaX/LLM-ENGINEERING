#Basic imports
import os
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
#Basic setup 
load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
openai=OpenAI()
MODEL="gpt-5-mini"

sys_prompt="""YOU ARE A HELPFUL ASSISTANT FOR AN AIRPLANE SERVICE KNOWN AS FLIGHT AI.
             MAKE THE RESPONSES SHORT IF YOU DON'T KNOW JUST SAY SO. NO MORE THAN 1 SENTENCE
             """
# ADDITIONAL DATA

tickets_price={"london":"$799","berlin":"$299","tokyo":"$399"}

# FUNCTION

def get_ticket_price(destination):
    print(f"Tool called for destination:{destination}")
    price=tickets_price.get(destination.lower(),"Unknown city")
    return f"Your price for {destination} is {price}"






"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
1. Required function to retrieve the supporting data
2. The passable json
3. To take care of the call 



XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

"""