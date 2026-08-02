import time

import requests
import os

os.system("anki &")

time.sleep(5)

url = "http://localhost:8765"

payload = {
    "action": "addNote",
    "version": 6,
    "params": {
        "note": {
            "deckName": "Deck A",
            "modelName": "Basic",
            "fields": {
                "Front": "Qual a capital do Brasil?",
                "Back": "Brasília"
            },
            "tags": ["python"]
        }
    }
}

response = requests.post(url, json=payload)

print(response.json())