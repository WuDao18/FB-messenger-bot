from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Your tokens (replace with actual values)
VERIFY_TOKEN = "my_secret_token_123"  # Choose any secret string
PAGE_ACCESS_TOKEN = "EAAIZC7vVAuAwBO4ZBa3JHqatZCCIvMnhg7GmmPwCYHOaj5tWHCdrYeZAEhkb4BxaMdZCfF8HD4udgfjO34E1AmP8vfr5lbdMZAQockZCyZByF1kotvMzATuy8awemPvK4AaIEQMoZAXG9XkSrK10s7Q5WoUXvR1xkwws4ATstIMC0IQp1k9QNEtBCgl5ZCsZACsCQZDZD"  # Get this from Facebook Developer Console

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
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT variable
    app.run(host="0.0.0.0", port=port, debug=True)
