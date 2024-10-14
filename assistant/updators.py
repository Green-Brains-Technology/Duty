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

    def clear_chat_history(self):
        # Load the data, clear the chat history, and write it back
        data = self._load_data()
        data["chathistory"] = data["chathistory"][:4]
        self._write_data(data)
    
    def clear_control_history(self):
        # Load the data, clear the control history, and write it back
        data = self._load_data()
        data["controlhistory"] = data["controlhistory"][:8]
        self._write_data(data)

