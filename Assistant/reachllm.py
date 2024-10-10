import speech_recognition as sr
import os
import google.generativeai as genai
import google.generativeai as genai
from histories import chathistory, controlhistory
import json
from controller import update_history
import sys
from talk import Talk
import asyncio


class ReachLLM:
    def __init__(self, api_key):
        self.api_key = "AIzaSyAQa03CGYA9B_ZdE78qz1oPrOO97iqU_F8"

        # Create the Generative Model with specific configurations
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            safety_settings=self.safety_settings,
            generation_config=self.generation_config,
        )
        genai.configure(api_key=self.api_key)

    def input_output(self, text):

        file_path = "histories.json"
        with open(file_path, "r") as file:
            data = json.load(file)
        
        talk = Talk()
        
        if text.startswith("midnight"):
            # remove midnight from beggining of the text
            text = text[8:]
            update_history(type = "control", role = "user", text = text)
            chat_session = self.model.start_chat(
                history=data["controlhistory"],
            )
            values = chat_session.send_message(text)
            response = values.text
            update_history(type = "control", role = "model", text = values.text)
            return response
        elif text == "java shutdown" or text == "shutdown" or text == "shutdown java":
            #await talk.speak_text(f"Shutting Down")
            print("Shutting Down...")
            sys.exit()
        else:
            update_history(type = "chat", role = "user", text = text)
            
            chat_session = self.model.start_chat(
                history=data["chathistory"],
            )
            values = chat_session.send_message(text)
            # remove all * from response
            response = values.text
            update_history(type = "chat", role = "model", text = values.text)
            return response.replace("*", "")


# Example usage
# if __name__ == "__main__":
#     reach_llm = ReachLLM(api_key="YOUR_API_KEY")

#     response = reach_llm.input_output("What's on my to-do list for today?")
#     print("Response from Gemini:\n", response)
