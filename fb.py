import os
import requests
from flask import Flask, request
import openai  # Make sure you have the OpenAI Python library installed

# Replace 'YOUR_PAGE_ACCESS_TOKEN' with your actual Page Access Token
page_access_token = 'EAAT2wmPxFhoBO2ca4Aswl3WRVMZA64C6928iEk1GceWKjehWI6W9rKmVvFXZAy3BMF1jSujXwFwiBdZAlVpfEWV8luTCijExG3jvKit5MZCZBnXp1259I79igcGNpebBAS6EkHTrR6sPjZBXy216i3tIfaEwMZAYZCadlOdOrfJejIPx4JOYBkqiIJKcr8bXncWS'

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API Key
openai_api_key = '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'

# Replace 'your_verify_token_here' with your actual Verify Token
VERIFY_TOKEN = 'ICT1202R42023'

# Initialize a Flask web server
app = Flask(__name__)

# Initialize the OpenAI API client
openai.api_key = openai_api_key

def send_message(user_id, message):
    message_data = {
        "recipient": {"id": user_id},
        "message": {"text": message}
    }
    response = requests.post(
        f"https://graph.facebook.com/v12.0/me/messages?access_token={page_access_token}",
        json=message_data
    )
    if response.status_code != 200:
        print("Failed to send message:", response.json())

# Generate a response using the OpenAI GPT-3 API
def generate_response(message_text):
    response = openai.Completion.create(
        engine="text-davinci-002",  # Use the engine that fits your needs
        prompt=message_text,
        max_tokens=50  # Adjust the maximum response length as needed
    )
    return response.choices[0].text

# Handle incoming messages from Messenger
def handle_message(event):
    user_id = event["sender"]["id"]
    message_text = event["message"]["text"]
    
    # Use the OpenAI GPT-3 API to generate a response based on message_text
    response_text = generate_response(message_text)
    
    # Send the response back to the user
    send_message(user_id, response_text)

# Route to verify the webhook during setup
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    hub_verify_token = request.args.get("hub.verify_token")
    hub_challenge = request.args.get("hub.challenge")
    
    # Verify the token
    if hub_verify_token == VERIFY_TOKEN:
        return hub_challenge, 200
    else:
        return "Verification failed", 403

# Route to handle incoming messages from Messenger
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for event in entry["messaging"]:
                if "message" in event:
                    handle_message(event)
    return "OK", 200

if __name__ == "__main__":
    app.run(port=9999)
