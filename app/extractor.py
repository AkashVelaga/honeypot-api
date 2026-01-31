import re
from typing import Dict, List
from app.schemas import Message


# --- Regex patterns (India-focused, adjustable) ---

UPI_REGEX = re.compile(r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b")
PHONE_REGEX = re.compile(r"\b(?:\+91[- ]?)?[6-9]\d{9}\b")
ACCOUNT_REGEX = re.compile(r"\b\d{9,18}\b")
URL_REGEX = re.compile(r"https?://[^\s]+")

SUSPICIOUS_KEYWORDS = {
    "urgent", "verify", "blocked", "suspended",
    "otp", "pin", "upi", "refund", "immediately"
}


def extract_intelligence(message: Message) -> Dict[str, List[str]]:
    """
    Extracts scam-related intelligence from a single message.
    """

    text = message.text.lower()

    intelligence = {
        "upiIds": list(set(UPI_REGEX.findall(text))),
        "phoneNumbers": list(set(PHONE_REGEX.findall(text))),
        "bankAccounts": list(set(ACCOUNT_REGEX.findall(text))),
        "phishingLinks": list(set(URL_REGEX.findall(text))),
        "suspiciousKeywords": [
            kw for kw in SUSPICIOUS_KEYWORDS if kw in text
        ]
    }

    return intelligence
