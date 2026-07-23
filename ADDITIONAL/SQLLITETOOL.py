import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import json
import sqlite3
load_dotenv(override=True)
api_key=os.getenv("OPENAI_API_KEY")
DB="prices.db"
with sqlite3.connect(DB) as conn:
    cursor=conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS prices (city TEXT PRIMARY KEY, price REAL)')
    conn.commit()
MODEL="gpt-5-mini"
openai=OpenAI()
sys_prompt="""
You are a helpful assistant for an Airline called FlighAI.
Give short, courteous answers, no more than one sentence. 
Always be accurate. If you don't know the answer, say so.
"""
#Starting part of the AirLINeAI

def set_ticket_price(city, price):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO prices (city, price) VALUES (?, ?) ON CONFLICT(city) DO UPDATE SET price = ?', (city.lower(), price, price))
        conn.commit()

ticket_prices={"london":"$799","paris":"$899","tokyo":"$1400","berlin":"$499"}
for city, price in ticket_prices.items():
    set_ticket_price(city, price)
#The function that will get called 
def get_ticket_price(city):
    print(f"Tool has been called for {city}")
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT price FROM prices WHERE city=?',(city.lower(),))
        result=cursor.fetchone()
        return f"Ticket price to city:${result[0]}" if result else " NO prices available for city in DB"
    
"""This defines the JSON"""

price_function={
    "name":"get_ticket_price",
    "description":"Get the price of a return ticket for selected destination",
    "parameters":{
        "type":"object",
        "properties":{
            "destination":{
                "type":"string",
                "description":"The city that customer wants to travel to"
            },
        },
        "required":["destination"],
        "additionalProperties":False

    }
}
tools=[{"type":"function","function":price_function}]
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
def handle_tool_calls(msg):
    responses=[]
    for tool_call in msg.tool_calls:
        if tool_call.function.name=="get_ticket_price":
             arguments=json.loads(tool_call.function.arguments)
             city=arguments.get('destination')
             price_details=get_ticket_price(city)
             responses.append({ "role":"tool","content":price_details,"tool_call_id":tool_call.id})
    return responses
def chat(msg,history):
    history=[{"role":h["role"],"content":h["content"]} for h in history]
    messages=[{"role":"system","content":sys_prompt}]+history+[{"role":"user","content":msg}]
    response=openai.chat.completions.create(model=MODEL,messages=messages,tools=tools)
    if response.choices[0].finish_reason=="tool_calls":
        message=response.choices[0].message
        tool_responses=handle_tool_calls(message)
        messages.append(message)
        messages.extend(tool_responses)
        response=openai.chat.completions.create(model=MODEL,messages=messages)
    return response.choices[0].message.content
gr.ChatInterface(fn=chat).launch(inbrowser=True)




"""
Tools:
        Allow frontier model to connect an external function
        1. Get deeper responses
        2. Ability to carry out actions within application
        3. Enhanced capabilities such as calculations
Theory:
        CODE -> <- LLM -> <- EXECUTE TOOL 
        EXECUTE TOOL -> <- CODE -> <- LLM 
        SO IT IS LIKE I SEND SOMETHING LLM TELLS TO CALL A TOOL
        THEN I CALL THE LLM WITH THE HISTORY AND SAYING YOU WANTED THIS 
        TOLL TO BE CALLED NOW GIVE ME THE ANSWER SO IT ISN'T LLM 
        RUNNING CODE IT IS THE CODE EXECUTED IT WHEN NEEDED BY THE 
        LLM AND CONTINUING FROM THAT PART FORWARD
Idea:
        IN THE SYSTEM PROMPT I TELL THE LLM THAT I HAVE THE ABILITY
        TO RUN SOME TOOL AND IF IT IS NEEDED TELL ME AND I'LL RUN
        THAT TOOL 
COMMON USE CASE:
                1. Fetch data or add knowledge or context
                2. Take action
                3. Perform calculations
                4. Modify UIs
                * A CALL TO ANOTHER LLM WHICH CAN BE DONE IN AGENTIC AIs
                * A ToDo list and track progress towards a goal 

Working:
        FOR AI TO USE THE TOOL IT HAS TO USE A JSON TO DESCRIBE IT AND THAT IT WILL USE
        IT IS WRITTEN IN A STANDARD WAY
"""