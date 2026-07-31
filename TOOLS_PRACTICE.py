"""
 STEPS TO TOOL CALLING:
 1. DEFINE A FUNCTION AND RELATED DATA ( MAYBE IN A DB OR LIST)
 2. DEFINE A JSON THAT WILL BE PASSED TO THE OPENAI CALL 
 3. HANDLE THE TOOL CALL 
"""


# BASIC IMPORTS

import os
from dotenv import load_dotenv
import json
from openai import OpenAI
import gradio as gr 

# Setting up the API

load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")
openai=OpenAI()

# DEFINING THE SYSTEM PROMPT AND THE TOOL FUNCTION 

MODEL="gpt-5-mini"
sys_prompt="""

    YOU ARE A HELPFUL ASSISSTANT FOR AN AIRPLANE CALLED FLIGHTY. 
    GIVE SHORT CONCISE ANSWERS NO MORE THAN ONE LINE. IF YOU DON'T KNOW
    THE ANSWER JUST SAY SO. 

"""

# THE DICTIONARY THAT WILL STORE THE PRICES OF FLIGHTS

prices={
    "london":"$799",
    "tokyo":"$500",
    "karachi":"$300"
}

def get_ticket_price(destination):
    print(f"THE FUNCTION IS CALLED FOR CITY {destination}")
    price=prices.get(destination.lower(),"Unknown city")
    if price=="Unknown city":
        return f"No price available for location : {destination}"
    return f"The price for the {destination} is {price}"

# DEFINING THE JSON 

price_function={
     "name":"get_ticket_price",
        "description":"Get the price of a ticket for selected destination",
        "parameters":{
            "type":"object",
            "properties":{
                "destination":{
                    "type":"string",
                    "description":"The city that customer wants to visit"
                },
            },
            "required":["destination"],
            "additionalProperties":False
        }
}


tools=[{"type":"function","function":price_function}]
# HANDLING THE TOOL CALL 

def handle_tool_call(msg):
    tool_call=msg.tool_calls[0]
    arguments=json.loads(tool_call.function.arguments)
    city=arguments.get('destination')
    price_details=get_ticket_price(city)
    response={
        "role":"tool",
        "content":price_details,
        "id":tool_call.id
    }
    return response
# CALLING OPENAI 

def chat(msg,history):
    history=[{"role":h["role"],"content":h["content"]} for h in history]
    messages=[{"role":"system","content":sys_prompt}]+history+[{"role":"user","content":msg}]
    response=openai.chat.completions.create(model=MODEL,messages=messages,tools=tools)
    if response.choices[0].finish_reason=="tool_calls":
        message=response.choices[0].message
        tool_response=handle_tool_call(message)
        messages.append(message)
        messages.extend(tool_response)
        response=openai.chat.completions.create(model=MODEL,messages=messages)
    return response.choices[0].message.content

# BASIC GRADIO CALL 

gr.ChatInterface(fn=chat).launch(inbrowser=True)