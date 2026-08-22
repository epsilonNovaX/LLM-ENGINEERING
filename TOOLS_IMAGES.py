from openai import OpenAI
import base64
import os
from dotenv import load_dotenv
load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
client = OpenAI()

prompt = """
A children's book drawing of a veterinarian using a stethoscope to
listen to the heartbeat of a tabbey cat. having white paws, stomach, and light green eyes, brownish green tabey, and white cheek area 
"""
#openai.chat.completions.create(model,messages)

result=client.images.generate(model="gpt-image-2",prompt=prompt)
#response=result.choices[0].message.content
image_base64=result.data[0].b64_json
#Just to decode the thing generated
image_bytes=base64.b64decode(image_base64)
#Just to write down
with open("tobey.png","wb") as f:
    f.write(image_bytes)

#Solution
"""
result = client.images.generate(model="gpt-image-2", prompt=prompt)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

# Save the image to a file
with open("otter.png", "wb") as f:
    f.write(image_bytes)
"""