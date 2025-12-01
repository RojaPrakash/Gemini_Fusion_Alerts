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

    sev_data = classify_severity(category, description)
    severity = sev_data.get("severity")
    reason = sev_data.get("reason")

    summary = generate_summary(category, severity, description)

    enriched = {
        "category": category,
        "confidence": confidence,
        "description": description,
        "severity": severity,
        "reason": reason,
        "summary": summary,
    }

    msg = (
        f"ALERT: {category.upper()}\n"
        f"Severity: {severity}\n"
        f"Confidence: {confidence}\n"
        f"Description: {description}"
    )

    send_sms(msg)

    return enriched
