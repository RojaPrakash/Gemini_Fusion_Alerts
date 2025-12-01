def call_gemini_model(model: str, prompt: str, image_bytes: bytes = None, context: dict = None):
    """
    MOCK implementation. Replace with real Gemini SDK calls later.
    Return a dict with expected fields used by vision/nlp_worker.
    """
    risk = 0.0
    lower = (prompt or "").lower()
    if "fire" in lower or "smoke" in lower:
        risk = 0.85
    elif "satellite" in lower:
        risk = 0.4
    else:
        risk = 0.1

    return {
        "model": model,
        "risk_score": round(risk, 2),
        "fire_prob": round(risk if risk > 0.5 else risk/2, 2),
        "smoke_prob": round(0.2 if "smoke" in lower else 0.05, 2),
        "labels": ["fire"] if "fire" in lower else (["smoke"] if "smoke" in lower else ["none"]),
        "explanation": "mocked response for demo; replace with real Gemini call"
    }
