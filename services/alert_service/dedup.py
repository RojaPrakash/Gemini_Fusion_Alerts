import time

# Store last alert details
_last_alert = None
_last_alert_time = 0
SUPPRESSION_WINDOW = 30  # seconds

def is_duplicate(alert: dict) -> bool:
    global _last_alert, _last_alert_time

    now = time.time()

    if _last_alert is None:
        _last_alert = alert
        _last_alert_time = now
        return False

    same_category = alert["category"] == _last_alert["category"]
    same_desc = alert["description"] == _last_alert["description"]

    if same_category and same_desc and (now - _last_alert_time) < SUPPRESSION_WINDOW:
        return True

    _last_alert = alert
    _last_alert_time = now
    return False
