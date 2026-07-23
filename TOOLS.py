#-----------------------------------------------------------This is the basic setup------------------------------------------------------------------------
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr

load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")
MODEL="gpt-5-mini"

sys_prompt="""YOU ARE A HELPFUL ASSISTANT FOR AN AIRPLANE SERVICE KNOWN AS FLIGHT AI.
             MAKE THE RESPONSES SHORT IF YOU DON'T KNOW JUST SAY SO. NO MORE THAN 1 SENTENCE
             """

openai=OpenAI()


#----------------------------------------------------------------------------------------------------------------------------------------------------------

"""
FOR TOOL CALL:
1. FUNCTION
2. JSON
3. ANY ADDITIONAL DATA FOR FUNCTION
"""

# ADDITIONAL DATA

tickets_price={"london":"$799","berlin":"$299","tokyo":"$399"}

# FUNCTION

def get_ticket_price(destination):
    print(f"Tool called for destination:{destination}")
    price=tickets_price.get(destination.lower(),"Unknown city")
    return f"Your price for {destination} is {price}"

# JSON

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
# THE PASSABLE JSON 
tools=[{"type":"function","function":price_function}]

#----------------------------------------------------------- THE OPENAI LOGIC FOR CALLING AND HANDLING THE TOOL CALL ----------------------------------------

#FIRST READ THE def chat function THEN DO THIS PART AS THIS RESOLVES FOR THE TOOL CALL

def handle_tool_call(msg):
    tool_call=msg.tool_calls[0]
    arguments=json.loads(tool_call.function.arguments)
    city=arguments.get('destination')
    price_details=get_ticket_price(city)
    response={
        "role":"tool",
        "content":price_details,
        "tool_call_id":tool_call.id
    }
    return response

# THIS IS TO ACCOUNT FOR MULTIPLE TOOL CALLS AS AN EXAMPLE SOMEONE CALLS FOR LONDON AND TOKYO 
def handle_tool_calls(msg):
    responses=[]
    for tool_call in msg.tool_calls:
        if tool_call.function.name=="get_ticket_price":
             arguments=json.loads(tool_call.function.arguments)
             city=arguments.get('destination')
             price_details=get_ticket_price(city)
             responses.append({ "role":"tool","content":price_details,"tool_call_id":tool_call.id})
    return responses


#THIS IS RELATED TO THE GRADIO CALL THAT IS PERFORMED AND THEN THE OPERATION TO SOLVE FOR THE TOOL CALL  

def chat(msg,history):
    history=[{"role":h["role"],"content":h["content"]} for h in history]
    messages=[{"role":"system","content":sys_prompt}]+history+[{"role":"user","content":msg}]
    response=openai.chat.completions.create(model=MODEL,messages=messages,tools=tools)
    # THIS IS THE PART THAT WILL KNOW SOLVE FOR THE TOOL CALLING 
    if response.choices[0].finish_reason=="tool_calls":
        message=response.choices[0].message

        #print(message) LOOK AT THE RELATED TEXT AT THE END FOR THIS 
        
        tool_responses=handle_tool_calls(message)
        messages.append(message)
        messages.extend(tool_responses)
        response=openai.chat.completions.create(model=MODEL,messages=messages)

    return response.choices[0].message.content
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------


gr.ChatInterface(fn=chat).launch(inbrowser=True)


"""
--------------------------------------------- GLOSSARY ----------------------------------------------------------------------------
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
Q: WHAT IS IN THE message=response.choices[0].message, print(message)
A:
ChatCompletionMessage(
    role='assistant',
    content=None,
    tool_calls=[
        ChatCompletionMessageToolCall(
            id='call_abc123',
            function=Function(
                name='get_weather',
                arguments='{"city":"London"}'
            ),
            type='function'
        )
    ]
)
THIS PROVIDES THE EXACT TOOL CALLS THAT HAVE TO BE PERFORMED 

In this case, since finish_reason == "tool_calls", the message won't contain a normal text response. Instead, it will contain the tool call(s) the model wants your program to execute.

It typically includes fields such as:

role → "assistant"
content → usually None or an empty string
tool_calls → a list of the function(s) the model wants to call, including:
the function name
the arguments
a unique tool call ID

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX



"""

"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX API CALLS XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
def get_ticket_price(destination):
    # Your existing ticket prices
    tickets_price = {
        "london": "$799",
        "berlin": "$299",
        "tokyo": "$399"
    }

    # Coordinates required by the weather API
    coordinates = {
        "london": (51.5072, -0.1276),
        "berlin": (52.5200, 13.4050),
        "tokyo": (35.6762, 139.6503)
    }

    price = tickets_price.get(destination.lower(), "Unknown city")

    if destination.lower() not in coordinates:
        return f"Your ticket price for {destination} is {price}."

    latitude, longitude = coordinates[destination.lower()]

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m"
        }
    )

    data = response.json()

    temperature = data["current"]["temperature_2m"]

    return (
        f"Your ticket price for {destination} is {price}. "
        f"The current temperature there is {temperature}°C."
    )
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


"""