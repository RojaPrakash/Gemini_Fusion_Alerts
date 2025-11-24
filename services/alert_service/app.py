from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from repository import AlertRepository
from dedup import is_duplicate
from logic import severity_nlp_logic



app = FastAPI()

# Allow frontend access (React dashboard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

repo = AlertRepository()


@app.get("/alerts")
def list_alerts():
    return repo.list_alerts()


@app.post("/alerts")
def create_alert(alert: dict):

    # 1️⃣ Avoid duplicates
    if is_duplicate(alert):
        return {"status": "duplicate_suppressed"}

    # 2️⃣ Enrich with severity + summary (Gemini)
    enriched_alert = severity_nlp_logic(alert)

    # 3️⃣ Save to in-memory store
    saved = repo.create_alert(enriched_alert)

    return {
        "status": "saved",
        "alert": saved
    }


@app.delete("/alerts/{alert_id}")
def delete_alert(alert_id: str):
    success = repo.delete_alert(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "deleted"}
