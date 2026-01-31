from fastapi import Header, HTTPException
from app.config import HONEYPOT_API_KEY

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != HONEYPOT_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
