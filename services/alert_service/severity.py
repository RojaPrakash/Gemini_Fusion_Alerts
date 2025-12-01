import os
import requests
import json
import re

GEMINI_TEXT_ENDPOINT = os.getenv("GEMINI_TEXT_ENDPOINT")


def _extract_json_block(text: str) -> str | None:
    """
    Extract first JSON object from model output.
    Handles fenced blocks like ```json { ... } ``` and plain { ... }.
    Returns the JSON string (including braces) or None.
    """
    if not text:
        return None

    # Look specifically for ```json { ... } ``` fences first
    m = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", text, flags=re.IGNORECASE)
    if m:
        return m.group(1)

    # Generic fenced code block ``` { ... } ```
    m = re.search(r"```\s*(\{[\s\S]*?\})\s*```", text, flags=re.IGNORECASE)
    if m:
        return m.group(1)

    # Direct JSON object anywhere in the text
    m = re.search(r"(\{[\s\S]*?\})", text, flags=re.DOTALL)
    if m:
        return m.group(1)

    return None


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

    try:
        r = requests.post(GEMINI_TEXT_ENDPOINT, json=payload, timeout=30)
        r.raise_for_status()
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("[Alert] Gemini call failed:", e)
        return {"severity": "UNKNOWN", "reason": f"api_error: {e}"}

    # Extract JSON block robustly
    json_block = _extract_json_block(text)
    if not json_block:
        print("[Alert] Failed to extract JSON from model output. Raw output:")
        print(text)
        return {"severity": "UNKNOWN", "reason": "parse_error", "raw": text}

    # Parse JSON safely
    try:
        parsed = json.loads(json_block)
        # Validate minimal shape
        if isinstance(parsed, dict) and "severity" in parsed:
            return parsed
        else:
            return {"severity": "UNKNOWN", "reason": "invalid_shape", "raw_parsed": parsed}
    except Exception as e:
        print("[Alert] JSON decode error:", e)
        print("[Alert] JSON block was:", json_block)
        return {"severity": "UNKNOWN", "reason": "json_decode_error", "error": str(e), "raw": json_block}
