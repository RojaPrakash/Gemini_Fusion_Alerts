🚨 Smart Disaster Detection System
Real-Time CCTV Disaster Detection using Gemini Flash Lite & Twilio SMS

This project is an end-to-end AI-powered disaster detection system built using microservices.
It continuously monitors CCTV frames, detects hazards such as fire, smoke, accidents, and triggers real-time SMS alerts using Twilio.

# 🔧 Prerequisites

- Docker + Docker Compose  
- Twilio account  
- Gemini API Key  
- Python 3.10+ (optional for local testing)

---

# 🔐 Environment Variables Setup

Create a `.env` file inside `infra/`:

```
GEMINI_API_KEY=xxxxxx
GEMINI_VISION_ENDPOINT=your vision model endpoint
GEMINI_TEXT_ENDPOINT=your text model endpoint

TWILIO_ACCOUNT_SID=xxxxxx
TWILIO_AUTH_TOKEN=xxxxxx
TWILIO_FROM_NUMBER=+1xxxxxxxx
TWILIO_TO_NUMBER=+91xxxxxxxx
```
---

#  How to Run the System

## 1️⃣ Add CCTV frames
Place `.jpg` / `.png` images in:

```
data/cctv_frames/
```

Examples:
- fire1.jpg  
- smoke.png  
- accident.jpg  
- normal.jpg  

These will be treated as simulated CCTV footage.
---

## 2️⃣ Start all services

From inside the infra/ folder:

```
docker-compose down
docker-compose up -d --build
```
This starts:
- fusion_worker  
- alert-service  
- cctv_fetcher  
---

# 🔍 Testing

## ✔ Check CCTV Fetcher

```
docker logs -f cctv_fetcher
```
Expected output:
```
[CCTV] Sending frame 1 to Fusion Worker...
```
---

## ✔ Check Fusion Worker

```
docker logs -f fusion_worker
```
Expected:
```
[Fusion] Detected fire with high confidence...
[Fusion] Alert pushed...
```
---

## ✔ Check Alert Service

```
docker logs -f alert-service
```
Expected output:

```
[SMS] Sent: 200 OK
```

---

## ✔ 4. Check Your Mobile

You should receive an SMS like:
```
🚨 EMERGENCY ALERT: FIRE DETECTED
Large fire detected through CCTV feed.
```
---

# 🤖 MCP Tools 

Located in `/mcp/` for agent integration:

- analyze_image.json  
- send_alert.json  
- detect_disaster.json  
- get_frame.json  
- list_frames.json  

These enable AI agents (ChatGPT, Cursor, VSCode AI) to use your microservices directly via MCP.
---
