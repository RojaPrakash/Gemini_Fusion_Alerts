import os
import requests

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM = os.getenv("TWILIO_FROM_NUMBER")
TO = os.getenv("TWILIO_TO_NUMBER")

def send_sms(text: str):
    if not (TWILIO_SID and TWILIO_TOKEN and FROM and TO):
        print("[SMS] Twilio config missing, skipping.")
        return

    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"

    data = {
        "From": FROM,
        "To": TO,
        "Body": text
    }

    try:
        r = requests.post(url, data=data, auth=(TWILIO_SID, TWILIO_TOKEN))
        print("[SMS] Sent:", r.status_code, r.text)
    except Exception as e:
        print("[SMS] Failed:", e)
