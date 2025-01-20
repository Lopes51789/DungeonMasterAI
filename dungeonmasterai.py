import os
from google import genai
from google.genai import types
import json

with open("settings.json") as f:
    settings = json.load(f)

API_KEY = settings["gemini"]["api key"]
client = genai.Client(api_key=[API_KEY])

client = genai.Client(
    vertexai=True, project="your-project-id", location="us-central1"
)

# Create the model
generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)