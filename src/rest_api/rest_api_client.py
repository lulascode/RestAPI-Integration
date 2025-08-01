import requests
import json
from dotenv import load_dotenv
import os

# prepare environment variables
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
EMAIL = os.getenv("EMAIL")

# set headers for requests
HEADERS = {"authtoken": AUTH_TOKEN}





# Requester-ID per E-Mail auflösen
def get_requester_id_by_email(email):
    url = f"{BASE_URL}/api/v3/users"
    response = requests.get(url, headers=HEADERS, verify=False)
    if response.status_code == 200:
        data = response.json()
        users = data.get("users", [])
        if users:
            return users[0]["id"]
    print(f"Fehler beim Abrufen der Requester-ID: {response.status_code} - {response.text}")
    return None





# 📨 Ticket mit Requester-ID erstellen
def create_ticket(subject, description, requester_id):
    url = f"{BASE_URL}/api/v3/requests"
    input_data = {
        "request": {
            "subject": subject,
            "description": description,
            "requester": {
                "id": requester_id
            },
            "status": {
                "name": "Erfasst"
            }
        }
    }
    data = {"input_data": json.dumps(input_data)}
    response = requests.post(url, headers=HEADERS, data=data, verify=False)
    return response





# ▶️ Hauptlogik
if __name__ == "__main__":
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
