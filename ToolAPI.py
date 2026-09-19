#BASIC IMPORTS 
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
#BASIC SETUP

load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
openai=OpenAI()
sys_prompt="""YOU ARE A HELPFUL ASSISTANT FOR AN AIRPLANE SERVICE KNOWN AS FLIGHT AI.
             MAKE THE RESPONSES SHORT IF YOU DON'T KNOW JUST SAY SO. NO MORE THAN 1 SENTENCE
             """
MODEL="gpt-5-mini"

# DEFINING THE FUNCTION THAT WILL BE CALLED

tickets_price={"london":"$799","berlin":"$299","tokyo":"$399"}


def get_ticket_price(destination):
    print(f"Tool called for destination:{destination}")
    price=tickets_price.get(destination.lower(),"Unknown city")
    return f"Your price for {destination} is {price}"


# DEFINE THE JSON

price_function={
    "name":"get_ticket_price",
    "description":"The function that returns the value for passed destination",
    "parameters":{
        "type":"object",
        "properties":{
            "destination":{
                "type":"string",
                "description":"The place for which we called the function"
            },
        },
        "required":["destination"],
        "additionalProperties":False
    }
}
#The passable JSON
tools=[{"type":"function","function":price_function}]


"""
1. THE IMPORTS
2. THE SETUP
3. FUNCTION TO BE CALLED
4. JSON TO BE PASSED
5. HANDLING THE TOOL CALL 
"""