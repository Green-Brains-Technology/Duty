import speech_recognition as sr
from talk import Talk
from listen import Listen
from reachllm import ReachLLM
import sys
import asyncio
from helpers import *
from updators import Updators
from pilot import Pilot
import threading


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
        await self.talk.speak_text(audioname="aud006", text=f"Welcome back, {self.username}! starting all services now .")

    
    async def activate(self):
        try:
            self.llmcontrol = ReachLLM(api_key="https")
            await self.talk.speak_text(audioname="aud007", text=f"{self.assistname} has initiated. Hello {self.username}. I will be on standby for your command.")
        except Exception as e:
            # Handle specific exceptions if needed, e.g., ValueError, TypeError, etc.
            print(f"Error occurred while recording: {e}")
            await self.talk.speak_text(audioname="aud008", text=f"Error setting up my Large Language Model. Restart the process or contact a software administrator")
        finally:
            await self.listener()
            
    async def scanprompt(self, text):        
        if text == "trinity clear the chat":
             await self.talk.speak_text(audioname="aud009", text=f"Chat history has been cleared.")
             self.updatorrs.clear_chat_history()
             self.updatorrs.clear_control_history()
             await self.listener()
        elif text == "shut down" or text == "shutdown":
             await self.shut_down()
    
    async def shut_down(self):
        await self.talk.speak_text(audioname="aud010", text=f"Alright, shutting down, bye.")
        print("Shutting Down...")
        self.updatorrs.clear_chat_history()
        self.updatorrs.clear_control_history()
        loop = asyncio.get_running_loop()
        loop.stop()
         

    async def listener(self):
        try:
            self.currprompt = self.listen.record_text()
            await self.scanprompt(self.currprompt)
        except Exception as e:
            print(f"Error occurred while recording: {e}")      
            await self.talk.speak_text(audioname="aud011", text=f"An error occurred while recording.")

        if self.currprompt.startswith(self.assistname):
            await self.talk.speak_text(audioname="aud012", text="Let me execute that for you.")
            self.updatorrs.update_control_user(self.currprompt)
            await self.controlrespond(self.currprompt)
        else:
            self.updatorrs.update_chat_user(self.currprompt)
            await self.chatrespond(self.currprompt)
    
    async def chatrespond(self, finalprompt):
        retry_count = 0  # Initialize retry counter
        max_retries = 2  # Maximum number of retries

        while retry_count <= max_retries:
            try:
                response = self.llmcontrol.input_output(finalprompt)
                break  # Exit the loop if successful
            except Exception as e:
                retry_count += 1  # Increment the retry counter
                await self.talk.speak_text(audioname="aud013", text=f"I am having trouble talking to the LLM online, attempt {retry_count}")
                print(f"{e}")

                if retry_count > max_retries:
                    await self.talk.speak_text(audioname="aud014", text="I was unable to connect after several attempts.")
                    await self.shut_down()  # Shutdown the application if maximum retries are reached
                    return  # Exit the function after maximum retries

        # If the response was successful, continue with the usual workflow
        speak_task = asyncio.create_task(self.talk.speak_text(audioname="aud015", text=response))
        
        # Start listening while the speak task runs
        listener_task = asyncio.create_task(self.listener())

        self.updatorrs.update_chat_model(response)

                
    async def controlrespond(self, finalprompt):
        retry_count = 0  # Initialize retry counter
        max_retries = 2  # Maximum number of retries

        while retry_count <= max_retries:
            try:
                response = self.llmcontrol.input_output(finalprompt)
                break  # Exit the loop if successful
            except Exception as e:
                retry_count += 1  # Increment the retry counter
                await self.talk.speak_text(audioname="aud016", text=f"I am having trouble talking to the LLM online, attempt {retry_count}")
                
                if retry_count > max_retries:
                    await self.talk.speak_text(audioname="aud017", text="I was unable to connect after several attempts.")
                    await self.shut_down()  # Shutdown the application if maximum retries are reached
                    return  # Exit the function after maximum retries

        # If the response was successful, continue with the usual workflow
        await self.copilot.execute(response)
        self.updatorrs.update_control_model(response)
        await self.listener()



                
            
        

    
    
