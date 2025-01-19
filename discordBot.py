from typing import Final
import os
from discord import Intents, Client, Message
import json


TOKEN = json.load(open("settings.json"))["discord"]["token"]
intents = Intents.default()
intents.message_content = True

client = Client(intents=intents)
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message was empty")
        return
    
    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else message.channel.send(response)
    except Exception as e:
        print(e)

def get_response(user_input: str) -> str:
    lowered = user_input.lower()

    if lowered == "hello":
        print("hello there")
    




def test():

    pass


if __name__ == "__main__":
    test()