from typing import List
from app.schemas import Message

URGENCY_KEYWORDS = {"urgent", "immediately", "blocked", "suspended"}
FINANCIAL_KEYWORDS = {"bank", "upi", "otp", "verify", "account"}

def detect_scam_intent(message: Message, history: List[Message]) -> float:
    text = message.text.lower()

    urgency_hits = sum(1 for k in URGENCY_KEYWORDS if k in text)
    financial_hits = sum(1 for k in FINANCIAL_KEYWORDS if k in text)

    score = 0.0
    if urgency_hits:
        score += 0.4
    if financial_hits:
        score += 0.4
    if urgency_hits and financial_hits:
        score += 0.2

    return round(min(score, 1.0), 2)
