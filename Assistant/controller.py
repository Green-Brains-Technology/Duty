import json
import os

DATA_FILE = 'app_data.json'

def save_user(user_name, ai_name):
    data = {
        'user_name': user_name,
        'ai_name': ai_name,
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return None

def update_history(type, role, text):
    # Load the existing JSON data
    file_path = "histories.json"
    with open(file_path, "r") as file:
        data = json.load(file)
    
    new_chat_history = {}
    new_control_history = {}

    # Define the new data to be added
    if type == "chat":
        if role == "user":
            new_chat_history = {
                "role": "user",
                "parts": [
                    text
                ]
            }
        else:
            new_chat_history = {
                "role": "model",
                "parts": [
                    text
                ]
                }
    else:
        if role == "user":
            new_control_history = {
                "role": "user",
                "parts": [
                    text
                ]
            }
        else:
            new_control_history = {
                "role": "model",
                "parts": [
                    text
                ]
            }

    # Append the new data to both histories
    if type == "chat":
        data["chathistory"].append(new_chat_history)
    else:
        data["controlhistory"].append(new_control_history)

    # Write the updated data back to the JSON file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
