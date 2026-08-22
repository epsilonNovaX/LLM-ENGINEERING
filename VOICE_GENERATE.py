import base64
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv(override=True)
os.getenv("OPENAI_API_KEY")
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-audio-1.5",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[{"role": "user", "content": "Is a tabey a good cat to keep at home?"}],
)

print(completion.choices[0])

wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
with open("dog.wav", "wb") as f:
    f.write(wav_bytes)