import os
import requests
import base64
import json
import time
import re

GEMINI_VISION_ENDPOINT = os.getenv("GEMINI_VISION_ENDPOINT")
ALERT_SERVICE_URL = os.getenv("ALERT_SERVICE_URL")

# ------------------------
# Helper: Extract JSON from Gemini 2.5 responses
# ------------------------
def extract_json_block(text):
    """
    Gemini 2.x usually responds with:

    ```json
    { ... }
    ```

    This function extracts the { ... } part.
    """
    # Look for fenced json block
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)

    # If the response directly starts with { ... }
    if text.strip().startswith("{"):
        return text

    return None


# ------------------------
# Retry wrapper
# ------------------------
def call_gemini_with_retry(payload, retries=5, delay=2):
    for attempt in range(1, retries + 1):
        try:
            r = requests.post(GEMINI_VISION_ENDPOINT, json=payload, timeout=20)

            if r.status_code == 429:
                print(f"[Fusion] Rate limit hit (attempt {attempt})")
                time.sleep(delay)
                continue

            r.raise_for_status()
            return r

        except Exception as e:
            print(f"[Fusion] Gemini error (attempt {attempt}): {str(e)}")
            time.sleep(delay)

    raise Exception("Gemini API failed after multiple retries")


# ------------------------
# Main processing
# ------------------------
def process_image(image_bytes: bytes):
    b64 = base64.b64encode(image_bytes).decode()

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are an emergency disaster detection model.\n"
                            "Detect if this image contains: fire, flood, collapse, accident, "
                            "landslide, chemical spill.\n"
                            "Return ONLY strict JSON in the following format:\n"
                            "{"
                            "  \"detected\": true/false,"
                            "  \"category\": \"fire|flood|collapse|accident|landslide|chemical|none\","
                            "  \"confidence\": number,"
                            "  \"description\": \"short text\""
                            "}"
                        )
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": b64
                        }
                    }
                ]
            }
        ]
    }

    # ---- Call Gemini ----
    try:
        response = call_gemini_with_retry(payload)
        data = response.json()
    except Exception as e:
        print("[Fusion] Gemini total failure:", e)
        return {
            "detected": False,
            "category": "none",
            "confidence": 0,
            "description": "gemini_error"
        }

    # ---- Extract JSON from Gemini output ----
    try:
        output_text = data["candidates"][0]["content"]["parts"][0]["text"]

        json_block = extract_json_block(output_text)
        if not json_block:
            raise ValueError("No JSON block found")

        result = json.loads(json_block)

    except Exception as e:
        print("[Fusion] JSON parse error:", e)
        return {
            "detected": False,
            "category": "none",
            "confidence": 0,
            "description": "parse_error",
            "raw": data
        }

    # ---- If disaster detected → Push alert ----
    if result.get("detected") is True:
        alert_payload = {
            "category": result["category"],
            "confidence": result["confidence"],
            "description": result["description"],
            "source": "fusion-worker"
        }

        try:
            r = requests.post(
                f"{ALERT_SERVICE_URL}/alerts",
                json=alert_payload,
                timeout=15
            )
            r.raise_for_status()
            print("[Fusion] Alert pushed:", r.json())

        except Exception as e:
            print("[Fusion] Failed to push alert:", e)

    return result