import os
import requests
import json

GEMINI_TEXT_ENDPOINT = os.getenv("GEMINI_TEXT_ENDPOINT")

def classify_severity(category, description):
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            f"Category: {category}. Description: {description}. "
                            "Classify severity as LOW, MEDIUM, HIGH and give a short reason. "
                            "Respond ONLY as JSON: {\"severity\": \"LOW|MEDIUM|HIGH\", \"reason\": \"...\"}"
                        )
                    }
                ]
            }
        ]
    }

    r = requests.post(GEMINI_TEXT_ENDPOINT, json=payload, timeout=30)
    r.raise_for_status()

    text = r.json()["candidates"][0]["content"]["parts"][0]["text"]

    return json.loads(text)
