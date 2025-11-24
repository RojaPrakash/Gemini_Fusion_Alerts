import json
from severity import classify_severity
from summary import generate_summary
from sms_notifier import send_sms


def severity_nlp_logic(alert: dict):
    """
    Takes a raw alert from fusion-worker and enriches it:
      - Adds severity using Gemini
      - Adds reason for severity
      - Adds human-readable summary
      - Sends SMS notification
    """

    category = alert.get("category")
    description = alert.get("description")
    confidence = alert.get("confidence")

    # 1️⃣ Use Gemini to classify severity
    sev_data = classify_severity(category, description)
    severity = sev_data.get("severity")
    reason = sev_data.get("reason")

    # 2️⃣ Use Gemini to generate summary
    summary = generate_summary(category, severity, description)

    # 3️⃣ Build enriched alert object
    enriched = {
        "category": category,
        "confidence": confidence,
        "description": description,
        "severity": severity,
        "reason": reason,
        "summary": summary,
    }

    # 4️⃣ Prepare SMS text
    msg = (
        f"ALERT: {category.upper()}\n"
        f"Severity: {severity}\n"
        f"Confidence: {confidence}\n"
        f"Description: {description}"
    )

    # 5️⃣ Send SMS
    send_sms(msg)

    return enriched
