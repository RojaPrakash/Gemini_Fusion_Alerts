from google import genai
from mcp_client import call_tool
import base64

# Initialize Gemini client
genai_client = genai.Client()

def handle_frame(image_bytes):
    """
    Main decision-making agent for CCTV frames.
    Uses gemini-flash-lite-latest for YES/NO gating,
    then calls MCP tools for analysis and alerting.
    """

    # Convert frame to base64 to send to MCP tool later
    b64 = base64.b64encode(image_bytes).decode()

    # Step 1: Ask Gemini (flash-lite) if we should analyze this frame
    decision_prompt = """
    You are a real-time disaster surveillance agent.
    The user will send CCTV frames.

    Identify if this frame needs further disaster analysis.
    Disasters include:
    - Fire
    - Smoke
    - Explosion
    - Accident
    - Flood
    - Building collapse
    - Hazardous situations

    Reply strictly with:
      yes
      or
      no
    """

    decision_result = genai_client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=[
            {"mime_type": "image/jpeg", "data": image_bytes},
            {"text": decision_prompt}
        ]
    )

    decision = decision_result.text.strip().lower()

    # If Gemini says "no", skip analysis
    if "yes" not in decision:
        return {
            "skipped": True,
            "decision": decision
        }

    # Step 2: Analyze using MCP analyze_image tool → Fusion Worker
    analysis = call_tool(
        "analyze_image",
        image_base64=b64
    )

    # Step 3: If disaster detected → trigger SMS alert via MCP send_alert tool
    if analysis.get("detected"):
        call_tool("send_alert", alert=analysis)

    return {
        "decision": decision,
        "analysis": analysis
    }
