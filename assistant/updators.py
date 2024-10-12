import json

class Updators:
    def __init__(self):
        self.file_path = "histories.json"
    
    def _load_data(self):
        # Load the existing JSON data
        with open(self.file_path, "r") as file:
            return json.load(file)
    
    def _write_data(self, data):
        # Write the updated data back to the JSON file
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
    
    def _update_history(self, history_type, role, text):
        # Load the current data
        data = self._load_data()

        # Create the new chat history structure
        new_chat_history = {
            "role": role,
            "parts": [text]
        }

        # Append the new chat history to the appropriate history type
        data[history_type].append(new_chat_history)

        # Write the updated data back to the file
        self._write_data(data)

    def update_chat_user(self, text):
        # Update the chat history for the user
        self._update_history("chathistory", "user", text)

    def update_chat_model(self, text):
        # Update the chat history for the model
        self._update_history("chathistory", "model", text)

    def update_control_user(self, text):
        # Update the control history for the user
        self._update_history("controlhistory", "user", text)

    def update_control_model(self, text):
        # Update the control history for the model
        self._update_history("controlhistory", "model", text)

# Usage example:
# manager = ChatHistoryManager("histories.json")
# manager.update_chat_user("Hello, how are you?")
# manager.update_chat_model("I'm doing well, thank you!")
# manager.update_control_user("Control message from user")
# manager.update_control_model("Control message from model")
