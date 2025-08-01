import os
from dotenv import load_dotenv
from bot.webex_bot import WebexBot
from rest_api.rest_api_client import create_ticket, get_requester_id_by_email

load_dotenv()

EMAIL = os.getenv("EMAIL")

def main():
    bot = WebexBot()
    bot.start()

    subject = "Test REST API"
    description = "Test-Ticket via REST API"

    requester_id = get_requester_id_by_email(EMAIL)

    if requester_id:
        print(f"Requester-ID für {EMAIL}: {requester_id}")
        response = create_ticket(subject, description, requester_id)
        print("Antwort vom SDP:")
        print(response.text)
    else:
        print(f"❌ Kein Requester mit der E-Mail {EMAIL} gefunden!")

if __name__ == "__main__":
    main()