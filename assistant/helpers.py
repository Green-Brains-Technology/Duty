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