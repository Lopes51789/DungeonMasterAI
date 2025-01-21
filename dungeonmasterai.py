import os
import google.generativeai as genai
import json
import time

with open("settings.json") as f:
    settings = json.load(f)

genai.configure(api_key=settings["gemini"]["api key"], transport="rest")

def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

# Create the model
generation_config = {
  "temperature": 1.5,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="""Pretend that you are a Dungeons and Dragons Dungeon Master. 
                        You are tasked to create a campaign for a party to play on.
                        First, you\'ll get the story limitations in a JSON file as well
                        as each of player's sheets also as JSON files. First, prompt 
                        the user to attach the story file and then the character sheets. 
                        Once you processed all of the files given, generate a rich story 
                        with a title and a clear objective that cannot changed 
                        regardless of the players actions. Present the beginning of 
                        the story in 2-3 very detailed paragraphs, with a clear premise 
                        that introduces the setting, the stakes, and the players\' 
                        shared motivation for working together along with why the characters
                        are together. Based on the characters sheets, evaluate if the action 
                        is possible and if not explain why and ask again for their input. 
                        If their action is categorized as [acrobatics, animal-handling, arcana, 
                        athletics, deception, history, insight, intimidation, investigation, 
                        medicine, nature, perception, performance, persuasion, religion, 
                        sleight-of-hand, stealth, survival], row a 20 sided die to see if the 
                        user would succeed in their action. You don't need to roll a dice for 
                        every action, only for the ones that fit the category. If they 
                        succeed, execute their action as intended, otherwise, feel free to 
                        disrupt their actions based on how low their roll on the die was
                        (1 is catastrofic, 2-5 is really bad, 6-9 is slighlty bad, 10-12 is ok,
                        13-15 is good, 16-19 is great, and 20 is perfect). The result of the 
                        dies are final and cannot be altered by the player. The framework 
                        of the history must start hidden and get uncovered as the players 
                        progress through the story. The story ends when the party achieves 
                        the final objective""",
)



chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("Hello")
print(response.text)
time.sleep(1)
files = [
  upload_to_gemini("story.json", mime_type="application/json"),
  upload_to_gemini("Char1.json", mime_type="application/json"),
]
wait_for_files_active(files)


while True:
    user_input = input("User: ")
    response = chat_session.send_message(user_input)
    print("Gemini: ", response.text)

