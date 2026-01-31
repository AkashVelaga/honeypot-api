from fastapi import FastAPI, Depends, Request
from datetime import datetime
import time
from collections import defaultdict
from types import SimpleNamespace

from app.security import verify_api_key
from app.detector import detect_scam_intent
from app.agent import generate_agent_reply
from app.extractor import extract_intelligence
from app.session_store import get_session, merge_intelligence
from app.callback import send_final_callback
from app.config import SCAM_CONFIDENCE_THRESHOLD

app = FastAPI(title="Agentic Honeypot API")

# --------------------------------------------------
# RATE LIMITING (SOFT)
# --------------------------------------------------
RATE_LIMIT = 10
RATE_WINDOW = 60
client_requests = defaultdict(list)


def is_rate_limited(client_id: str):
    now = time.time()
    window = client_requests[client_id]
    client_requests[client_id] = [t for t in window if now - t < RATE_WINDOW]

    if len(client_requests[client_id]) >= RATE_LIMIT:
        return True

    client_requests[client_id].append(now)
    return False


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# --------------------------------------------------
# GUVI GET PROBE
# --------------------------------------------------
@app.get("/honeypot/message")
def honeypot_get():
    return {
        "status": "success",
        "scamDetected": False,
        "reply": "Honeypot API is ready.",
        "confidenceScore": 0.0
    }


# --------------------------------------------------
# MAIN POST ENDPOINT (FINAL, FIXED)
# --------------------------------------------------
@app.post("/honeypot/message")
async def honeypot_post(
    request: Request,
    api_key=Depends(verify_api_key)
):
    # ----------------------------------------------
    # RATE LIMIT
    # ----------------------------------------------
    client_ip = request.client.host
    if is_rate_limited(client_ip):
        return {
            "status": "success",
            "scamDetected": False,
            "reply": "Please wait a moment before continuing.",
            "confidenceScore": 0.0
        }

    # ----------------------------------------------
    # SAFE BODY PARSE
    # ----------------------------------------------
    try:
        payload = await request.json()
    except Exception:
        payload = {}

    # ----------------------------------------------
    # EXTRACT RAW TEXT
    # ----------------------------------------------
    raw_text = ""

    if isinstance(payload, str):
        raw_text = payload.strip()

    elif isinstance(payload, dict):
        msg = payload.get("message")
        if isinstance(msg, str):
            raw_text = msg.strip()
        elif isinstance(msg, dict):
            raw_text = (
                msg.get("text")
                or msg.get("message")
                or ""
            ).strip()

    # ----------------------------------------------
    # PREFLIGHT / NO CONTENT
    # ----------------------------------------------
    if not raw_text:
        return {
            "status": "success",
            "scamDetected": False,
            "reply": "Honeypot API is ready.",
            "confidenceScore": 0.0
        }

    # ----------------------------------------------
    # NORMALIZE MESSAGE (DICT)
    # ----------------------------------------------
    session_id = payload.get("sessionId") or "guvi-session"

    message_dict = {
        "sender": "scammer",
        "text": raw_text,
        "timestamp": datetime.utcnow().isoformat()
    }

    # 🔥 CRITICAL FIX: convert dict → object
    message = SimpleNamespace(**message_dict)

    # ----------------------------------------------
    # SESSION
    # ----------------------------------------------
    session = get_session(session_id)
    session.total_messages += 1

    history = payload.get("conversationHistory") or []
    history.append(message)

    # ----------------------------------------------
    # SCAM DETECTION
    # ----------------------------------------------
    score = detect_scam_intent(message, history)

    text_lower = raw_text.lower()
    scam_detected = (
        score >= SCAM_CONFIDENCE_THRESHOLD
        or any(k in text_lower for k in [
            "otp", "upi", "account", "bank",
            "blocked", "suspended", "verify",
            "urgent", "compromised"
        ])
    )

    # ----------------------------------------------
    # AGENT RESPONSE
    # ----------------------------------------------
    if scam_detected:
        reply = generate_agent_reply(message, history)
    else:
        reply = "Okay, can you explain a bit more?"

    # ----------------------------------------------
    # INTELLIGENCE EXTRACTION
    # ----------------------------------------------
    extracted = extract_intelligence(message)
    merge_intelligence(session.intelligence, extracted)

    # ----------------------------------------------
    # FINAL CALLBACK
    # ----------------------------------------------
    if scam_detected and session.total_messages >= 5 and not session.completed:
        send_final_callback(
            session_id,
            session.total_messages,
            session.intelligence
        )
        session.completed = True

    # ----------------------------------------------
    # RESPONSE
    # ----------------------------------------------
    return {
        "status": "success",
        "scamDetected": scam_detected,
        "reply": reply,
        "confidenceScore": round(score, 2)
    }
