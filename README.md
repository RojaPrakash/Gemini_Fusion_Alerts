🚨 Smart Disaster Detection System Real-Time CCTV Disaster Intelligence using Gemini 2.5 Flash + Twilio SMS + AI Agents

This project is an end-to-end AI-powered, agent-enabled disaster detection system built using microservices. It continuously monitors CCTV frames (simulated or real), detects hazards such as fire, flood, accidents, chemical spills, collapses, and triggers real-time SMS alerts using Twilio.

It is fully containerized, lightweight, and ready for real-world integration with live CCTV streams.

🔧 Prerequisites

Docker + Docker Compose

Twilio account with SMS trial/paid number

Gemini API Key (must support gemini-2.5-flash)

Python 3.10+ (optional for local testing)

Internet access for Gemini & Twilio APIs

🔐 Environment Variables Setup

Create a .env file inside infra/:

GEMINI_API_KEY=xxxxxxx GEMINI_VISION_ENDPOINT=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=xxxxxx GEMINI_TEXT_ENDPOINT=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=xxxxxx

TWILIO_ACCOUNT_SID=xxxxxx TWILIO_AUTH_TOKEN=xxxxxx TWILIO_FROM_NUMBER=+1xxxxxxxx TWILIO_TO_NUMBER=+91xxxxxxxx

⚠ Note: Gemini 2.5 Flash is required because earlier Flash-Lite endpoints were deprecated.

▶️ How to Run the System 1️⃣ Add CCTV frames

Place frames inside:

data/cctv_frames/

Examples:

fire.png

flood.png

accident.jpg

safe.jpg

These simulate a CCTV camera feed.

2️⃣ Start all services

From inside infra/ directory:

docker-compose down docker-compose up -d --build

This starts:

fusion_worker (Gemini vision analysis)

alert-service (severity reasoning + SMS)

cctv_fetcher (simulated CCTV feed)

🔍 Testing & Logs ✔ CCTV Fetcher docker logs -f cctv_fetcher

Example:

[CCTV] Sending frame fire.png [CCTV] Fusion response: {...}

✔ Fusion Worker docker logs -f fusion_worker

Expected:

[Fusion] Detected fire with confidence 0.98 [Fusion] Alert pushed

✔ Alert Service docker logs -f alert-service

Expected:

[SMS] Sent: 201

✔ Check Your Mobile

You will receive:

🚨 ALERT: FIRE DETECTED Severity: HIGH Confidence: 0.98 Description: A vehicle is engulfed in flames.

🤖 MCP Tools (Agent Integration)

Located inside /mcp/:

analyze_image.json

detect_disaster.json

send_alert.json

list_frames.json

get_frame.json

These allow AI agents (ChatGPT, Cursor, VSCode AI) to:

Fetch frames

Analyze images

Trigger alerts

Orchestrate workflows
