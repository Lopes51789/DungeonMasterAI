from openai import OpenAI
import json

"""with open("settings.json", "r") as f:
    config = f."""
client = OpenAI()
completion = client.chat.completions.create(
    model="gpt-4o",
    store=True,
    messages=[
        {"role": "user", "content": "write a haiku about ai"}
    ]
)

print(completion.choices[0].message)
