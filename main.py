# Speech to text and text to speech with Gemini API

import speech_recognition as sr
import asyncio
from reachllm import ReachLLM
from talk import Talk
from listen import Listen
from midnight import Midknight

talk = Talk()
reach_llm = ReachLLM(api_key="YOUR_API_KEY")
listen = Listen()

# Main loop starting here
print("Initializing Knight ...")

asyncio.run(talk.speak_text("Knight has initiated. Hello Fredrick. I will be on standby for your command."))
while True:
    prompt = listen.record_text()
    # check if prompt begins with the word "midnight"
    if prompt.startswith("midnight"):
        asyncio.run(talk.speak_text("Handing over to Midnight."))
        midnight = Midknight(prompt)
    else:
        response = reach_llm.input_output(prompt)
        response = response.replace("*", " ")
        asyncio.run(talk.speak_text(response))