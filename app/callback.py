import requests
from app.config import GUVI_CALLBACK_URL


def send_final_callback(
    session_id: str,
    total_messages: int,
    intelligence: dict
):
    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": total_messages,
        "extractedIntelligence": intelligence,
        "agentNotes": "Used urgency and payment redirection tactics"
    }

    try:
        requests.post(
            GUVI_CALLBACK_URL,
            json=payload,
            timeout=5
        )
    except Exception:
        # Silent fail: do NOT crash the API
        pass
