# 🚨 Smart Disaster Detection System
Real-Time CCTV Disaster Detection using **Gemini 2.5 Flash** & **Twilio SMS**

This project is an end-to-end **AI‑powered**, **microservice-based** disaster detection system.  
It continuously monitors CCTV frames (simulated or real), identifies hazards such as **fire, flood, accidents, collapses, chemical spills**, and sends **real‑time SMS alerts** using Twilio.

---

## 🔧 Prerequisites

- Docker & Docker Compose  
- Gemini API Key (**must support gemini-2.5-flash**)  
- Twilio account (Trial or Production)  
- Python 3.10+ (optional for local testing)

---

## 🔐 Environment Variables Setup

Create a file `.env` inside `infra/`:

```
GEMINI_API_KEY=xxxxxx
GEMINI_VISION_ENDPOINT=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=xxxxxx
GEMINI_TEXT_ENDPOINT=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=xxxxxx

TWILIO_ACCOUNT_SID=xxxxxx
TWILIO_AUTH_TOKEN=xxxxxx
TWILIO_FROM_NUMBER=+1xxxxxxxx
TWILIO_TO_NUMBER=+91xxxxxxxx
```

⚠️ **Important:** Older models like `flash-lite-latest` are deprecated and return **404**.  
✔ Use **gemini-2.5-flash** for both VISION & TEXT reasoning.

---

## ▶️ How to Run the System

### **1️⃣ Add CCTV Frames**

Place `.jpg` / `.png` images inside:

```
data/cctv_frames/
```

Examples:
- fire.png  
- flood.png  
- accident.jpg  
- safe.jpg  

These simulate a CCTV feed.

---

### **2️⃣ Start All Services**

Inside the `infra/` directory:

```
docker-compose down
docker-compose up -d --build
```

This starts:

- 🧠 **fusion_worker** (Gemini vision analysis)  
- 📢 **alert-service** (severity analysis + SMS)  
- 🎥 **cctv_fetcher** (CCTV frame simulator)  

---

## 🔍 Testing

### ✔ CCTV Fetcher Logs  
```
docker logs -f cctv_fetcher
```
Expected:
```
[CCTV] Sending frame fire.png
```

### ✔ Fusion Worker Logs  
```
docker logs -f fusion_worker
```
Expected:
```
[Fusion] Detected fire with confidence 0.98
[Fusion] Alert pushed
```

### ✔ Alert Service Logs  
```
docker logs -f alert-service
```
Expected:
```
[SMS] Sent: 201 {"status":"queued", ...}
```

### ✔ SMS Received  
Example message:
```
🚨 ALERT: FIRE DETECTED
Severity: HIGH
Confidence: 0.98
Description: A vehicle is engulfed in flames.
```

---

# 🤖 MCP Tools (Agent Integration)

Located in `/mcp/`:

- analyze_image.json  
- detect_disaster.json  
- send_alert.json  
- list_frames.json  
- get_frame.json  

These allow **AI Agents** (ChatGPT, Cursor, VSCode AI) to call your microservices directly.

---

#  System Architecture (High-Level)

The agent pipeline follows:

### **Perception → Reasoning → Action**

1. **Perception**  
   Gemini 2.5 Flash Vision analyzes CCTV frames.

2. **Reasoning**  
   Text model classifies severity (LOW / MEDIUM / HIGH).

3. **Action**  
   Alert service sends SMS via Twilio.

4. **MCP Integration**  
   Tools allow autonomous multi-agent orchestration.

5. **Microservices**  
   Docker-based modular design for scalability.

---

# 🎯 Summary

This system demonstrates a **production-ready**, **agent‑enabled** AI pipeline capable of:  
✔ Real-time CCTV monitoring  
✔ AI hazard detection  
✔ Severity reasoning  
✔ SMS alert escalation  
✔ MCP‑powered multi-agent integration  

Perfect for **safety automation**, **smart cities**, **industrial monitoring**, and **AI agent workflows**.

