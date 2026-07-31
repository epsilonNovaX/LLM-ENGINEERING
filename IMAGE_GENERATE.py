from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import requests
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.images.generate(
    model="gpt-image-1",
    prompt="A vibrant pop-art view of New York City with famous landmarks.",
    size="1024x1024",
)

# Depending on your SDK version, this may return a URL or image bytes.
print(response)