import os
from dotenv import load_dotenv

load_dotenv()

HONEYPOT_API_KEY = os.getenv("HONEYPOT_API_KEY")
SCAM_CONFIDENCE_THRESHOLD = float(os.getenv("SCAM_CONFIDENCE_THRESHOLD", 0.6))
GUVI_CALLBACK_URL = os.getenv("GUVI_CALLBACK_URL")

if not HONEYPOT_API_KEY:
    raise RuntimeError("HONEYPOT_API_KEY not set")
