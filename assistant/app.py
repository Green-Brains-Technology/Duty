import speech_recognition as sr
from talk import Talk
from listen import Listen
from reachllm import ReachLLM
import sys
import asyncio
from helpers import *
from updators import Updators
from pilot import Pilot

class AssistCore:
    def __init__(self, data):
        self.assistname = data['ai_name']
        self.username = data['user_name']
        self.currprompt = ""
        self.talk = Talk()
        self.listen = Listen()
        self.copilot = Pilot()
        self.updatorrs = Updators()
        self.llmcontrol = None
        asyncio.create_task(self.startup())  # Start the async initialization
        
    
    async def startup(self):
        await self.check_microphone()
        
    
    async def check_microphone(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
        except sr.RequestError:
            await self.talk.speak_text(audioname="aud003", text="Could not request results from speech recognition service")
        except:
            await self.talk.speak_text(audioname="aud004", text="Microphone not found or not working")

    
    async def new_greet(self):
        await self.talk.speak_text(audioname="aud005", text=f"Welcome {self.username}! starting all services now .")

    async def greet(self):
        await self.talk.speak_text(audioname="aud005", text=f"Welcome back, {self.username}! starting all services now .")

    
    async def activate(self):
        try:
            self.llmcontrol = ReachLLM(api_key="https")
            await self.talk.speak_text(audioname="aud006", text=f"{self.assistname} has initiated. Hello {self.username}. I will be on standby for your command.")
        except Exception as e:
            # Handle specific exceptions if needed, e.g., ValueError, TypeError, etc.
            print(f"Error occurred while recording: {e}")
            await self.talk.speak_text(audioname="aud007", text=f"Error setting up my Large Language Model. Restart the process or contact a software administrator")
        finally:
            await self.listener()
            
    async def scanprompt(self, text):
        if text == "shut down" or text == "shutdown":
                await self.talk.speak_text(audioname="close", text=f"Alright, shutting down, bye.")
                print("Shutting Down...")
                
                loop = asyncio.get_running_loop()
                loop.stop()
                sys.exit()

    async def listener(self):
        try:
            self.currprompt = self.listen.record_text()
            await self.scanprompt(self.currprompt)
            self.updatorrs.update_chat_user(self.currprompt)
        except Exception as e:
            print(f"Error occurred while recording: {e}")      
            await self.talk.speak_text(audioname="aud008", text=f"An error occurred while recording.")

        if self.currprompt.startswith(self.assistname):
            await self.talk.speak_text(audioname="aud009", text="Let me execute that for you.")
            await self.copilot.execute(self.currprompt[len(self.assistname):])
            await self.listener()
        else:
            await self.respond()
             
    async def respond(self):
        try:
                response = self.llmcontrol.input_output(self.currprompt)
        except Exception as e:
                await self.talk.speak_text(audioname="aud010", text=f"I am having trouble talking to the LLM online")
                print(f"Error occurred while recording: {e}")
        finally:
                response = response.replace("*", " ")
                await self.talk.speak_text(audioname="aud011", text=response)
                self.updatorrs.update_chat_model(response)

                
                await self.listener()


                
            
        

    
    
