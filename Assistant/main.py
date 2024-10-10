# Speech to text and text to speech with Gemini API

import speech_recognition as sr
import asyncio
from reachllm import ReachLLM
from talk import Talk
from listen import Listen
from midnight import Midknight
from controller import load_data, save_user

talk = Talk()
reach_llm = ReachLLM(api_key="YOUR_API_KEY")
listen = Listen()

# Check if microphone is working
def check_microphone():
    r = sr.Recognizer()
    try:
         with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
         print("Microphone is working")
    except sr.RequestError:
         print("Could not request results from speech recognition service")
    except:
         print("Microphone not found or not working")

#Asking for user input
async def assistant_set_up(talk, listen):
    await talk.speak_text("You need to set up this personal assistant before using it. Firstly, What is your name? say only the name you want the assistant to call you.")
    user_name = listen.record_text()
    await talk.speak_text(f"Nice to meet you, {user_name}. What would you like to call me?")
    ai_name = listen.record_text()
    return user_name, ai_name

async def main():
    talk = Talk()
    listen = Listen()
    
    check_microphone()
    
    data = load_data()
    
    if data:
        user_name = data['user_name']
        ai_name = data['ai_name']
        await talk.speak_text(f"Welcome back, {user_name}! starting all services now .")
    else:
        user_name, ai_name = await assistant_set_up(talk, listen)
        save_user(user_name, ai_name)
    
    reach_llm = ReachLLM(api_key="YOUR_API_KEY")
    reach_llm.user_name = user_name
    reach_llm.ai_name = ai_name
    
    await talk.speak_text(f"{ai_name} has initiated. Hello {user_name}. I will be on standby for your command.")
    
    while True:
        prompt = listen.record_text()
        if prompt.startswith("midnight"):
            await talk.speak_text("Handing over to Midnight.")
            midnight = Midknight(prompt)
        else:
            response = reach_llm.input_output(prompt)
            response = response.replace("*", " ")
            await talk.speak_text(response)

if __name__ == "__main__":
    asyncio.run(main())