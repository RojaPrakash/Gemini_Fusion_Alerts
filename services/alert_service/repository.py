import uuid
from threading import Lock

class AlertRepository:
    def __init__(self):
        self.store = {}
        self.lock = Lock()

    def list_alerts(self):
        with self.lock:
            return list(self.store.values())

    def create_alert(self, alert: dict):
        alert_id = str(uuid.uuid4())
        alert_record = {"id": alert_id, **alert}
        with self.lock:
            self.store[alert_id] = alert_record
        return alert_record

    def delete_alert(self, alert_id: str) -> bool:
        with self.lock:
            if alert_id in self.store:
                del self.store[alert_id]
                return True
            return False
