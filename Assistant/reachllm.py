import google.generativeai as genai
import google.generativeai as genai
import json
from helpers import load_data



class ReachLLM:
    def __init__(self, api_key):
        self.api_key = "AIzaSyBHSfYFa_MqLGDb2GLC0YxGKHxSJfelBFQ"

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
        
        appdata = load_data()
        
        if text.startswith(appdata["ai_name"]):
            # remove midnight from beggining of the text
            text = text[len(appdata['ai_name']):]
            finalcontrolprompt = (f"generate the python code to {text} on windows, do not add any comment, just return code syntax. adding any comment will crush the app")
            
            chat_session = self.model.start_chat(
                history=data["controlhistory"],
            )
            values = chat_session.send_message(finalcontrolprompt)
            response = values.text
            return response
        else:
            finalchatprompt = text
            chat_session = self.model.start_chat(
                history=data["chathistory"],
            )
            values = chat_session.send_message(finalchatprompt)
            # remove all * from response
            response = values.text
            return response.replace("*", "")


# Example usage
# if __name__ == "__main__":
#     reach_llm = ReachLLM(api_key="YOUR_API_KEY")

#     response = reach_llm.input_output("What's on my to-do list for today?")
#     print("Response from Gemini:\n", response)
