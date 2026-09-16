#BASIC IMPORTS 
import os
from dotenv import load_dotenv
from openai import OpenAI
#BASIC SETUP

load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
openai=OpenAI()
sys_prompt="""YOU ARE A HELPFUL ASSISTANT FOR AN AIRPLANE SERVICE KNOWN AS FLIGHT AI.
             MAKE THE RESPONSES SHORT IF YOU DON'T KNOW JUST SAY SO. NO MORE THAN 1 SENTENCE
             """
MODEL="gpt-5-mini"

#

"""
1. THE IMPORTS
2. THE SETUP
3. FUNCTION TO BE CALLED
4. JSON TO BE PASSED
5. HANDLING THE TOOL CALL 
"""