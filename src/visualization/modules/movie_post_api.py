import requests

API_ENDPOINT = "http://localhost:8000/chat"

def send_chat_request(prompts):
    response = requests.post(API_ENDPOINT, json={"question": prompts})
    return response.json()