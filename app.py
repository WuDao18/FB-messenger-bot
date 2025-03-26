from flask import Flask, request
import requests

app = Flask(__name__)

# Your tokens (replace with actual values)
VERIFY_TOKEN = "my_secret_token_123"  # Choose any secret string
PAGE_ACCESS_TOKEN = "EAAIZC7vVAuAwBO69ucAVEGFZCNIURTLu2wppzajpwXoZC7yZCnywnYLJtGe0GGBfS97aQT6T8PEgZCxeiVrtrqIh7uI7pf6zjINyoS1SQyAGjOZAE7vpZCjq6AhPqRrpkZAqPEJ1Wp8pDcCh958njP4ieDzWUYkET15hAjomFBVZBHl6hGTVKVZC4JASdURcoxwAZDZD"  # Get this from Facebook Developer Console

@app.route("/", methods=["GET"])
def home():
    return "Messenger Bot is Running!"

# Webhook verification (Facebook will call this to verify)
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token_sent == VERIFY_TOKEN:
        return challenge
    return "Invalid verification token", 403

# Webhook to receive messages
@app.route("/webhook", methods=["POST"])
def handle_messages():
    data = request.get_json()

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if "message" in messaging_event:
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"].get("text", "")

                    send_message(sender_id, f"Echo: {message_text}")

    return "Message received", 200

# Function to send messages back to users
def send_message(recipient_id, message_text):
    url = "https://graph.facebook.com/v18.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
    }

    response = requests.post(url, params=params, json=data, headers=headers)
    return response.json()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
