🚨 Smart Disaster Detection System
Real-Time CCTV Disaster Detection using Gemini 2.5 Flash & Twilio SMS

This project is an end-to-end AI-powered, microservice-based disaster detection system.
It continuously monitors CCTV frames (simulated or real), identifies hazards such as fire, flood, accidents, collapses, chemical spills, and sends real-time SMS alerts using Twilio.

🔧 Prerequisites

Docker & Docker Compose

Gemini API Key (must support gemini-2.5-flash)

Twilio account with active Trial/Production Number

Python 3.10+ (optional for local testing)

🔐 Environment Variables Setup

Create a file .env inside infra/:

GEMINI_API_KEY=xxxxxx
GEMINI_VISION_ENDPOINT=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=xxxxxx
GEMINI_TEXT_ENDPOINT=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=xxxxxx

TWILIO_ACCOUNT_SID=xxxxxx
TWILIO_AUTH_TOKEN=xxxxxx
TWILIO_FROM_NUMBER=+1xxxxxxxx
TWILIO_TO_NUMBER=+91xxxxxxxx


⚠️ Important: Earlier models like flash-lite-latest are deprecated and return 404.
Use only gemini-2.5-flash.

▶️ How to Run the System
1️⃣ Add CCTV Frames

Place .jpg / .png images inside:

data/cctv_frames/


Example files:

fire.png

flood.png

accident.jpg

safe.jpg

These will act as simulated CCTV feed.

2️⃣ Start All Services

From infra/ directory:

docker-compose down
docker-compose up -d --build


This starts:

fusion_worker (Gemini vision analysis)

alert-service (severity + SMS)

cctv_fetcher (CCTV frame simulator)

🔍 Testing
✔ CCTV Fetcher Logs
docker logs -f cctv_fetcher


Expected:

[CCTV] Sending frame fire.png

✔ Fusion Worker Logs
docker logs -f fusion_worker


Expected:

[Fusion] Detected fire with confidence 0.98
[Fusion] Alert pushed

✔ Alert Service Logs
docker logs -f alert-service


Expected:

[SMS] Sent: 201 {"status":"queued", ...}

✔ SMS Received

Example message:

🚨 ALERT: FIRE DETECTED
Severity: HIGH
Confidence: 0.98
Description: A vehicle is engulfed in flames.

🤖 MCP Tools (for Agent Support)

Located in /mcp/:

analyze_image.json

detect_disaster.json

send_alert.json

list_frames.json

get_frame.json

These allow AI Agents (ChatGPT, Cursor, VSCode AI) to call your microservices directly using tool invocation.

# 🧠 How the System Works (Architecture Overview)

This system follows the classic intelligent-agent pipeline of: Perception → Reasoning → Action:

Gemini 2.5 Flash Vision → Detect hazards

Text Reasoning Agent → Classify severity

Alert Service → Trigger SMS

MCP Tools → AI agent orchestration

Docker Microservices → Scalable architecture
