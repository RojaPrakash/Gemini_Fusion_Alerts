import os
import requests

GEMINI_TEXT_ENDPOINT = os.getenv("GEMINI_TEXT_ENDPOINT")

def generate_summary(category, severity, description):
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            f"Category: {category}, Severity: {severity}. "
                            f"Description: {description}. "
                            "Create a short emergency alert message."
                        )
                    }
                ]
            }
        ]
    }

    r = requests.post(GEMINI_TEXT_ENDPOINT, json=payload, timeout=30)
    r.raise_for_status()

    return r.json()["candidates"][0]["content"]["parts"][0]["text"]
