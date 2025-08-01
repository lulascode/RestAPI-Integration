from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI
from rest_api.rest_api_client import create_ticket, get_requester_id_by_email
import os

app = Flask(__name__)
api = WebexTeamsAPI(access_token=os.getenv("WEBEX_ACCESS_TOKEN"))

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if 'data' in data:
        room_id = data['data']['roomId']
        person_id = data['data']['personId']
        message_id = data['data']['id']

        # Get the message content
        message = api.messages.get(message_id)
        text = message.text

        # Process the message and create a ticket if needed
        if "create ticket" in text.lower():
            subject = "Ticket from Webex"
            description = "This ticket was created via Webex bot."
            requester_id = get_requester_id_by_email(os.getenv("EMAIL"))

            if requester_id:
                response = create_ticket(subject, description, requester_id)
                api.messages.create(room_id, text=f"Ticket created: {response.text}")
            else:
                api.messages.create(room_id, text="❌ No requester found with the provided email.")
        else:
            api.messages.create(room_id, text="I can help you create a ticket. Just say 'create ticket'.")

    return jsonify({'status': 'ok'}), 200

if __name__ == "__main__":
    app.run(port=5000)