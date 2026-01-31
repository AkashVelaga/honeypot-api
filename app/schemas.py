from pydantic import BaseModel, Extra
from typing import List, Optional


class Message(BaseModel):
    sender: Optional[str] = None
    text: Optional[str] = None
    timestamp: Optional[str] = None

    class Config:
        extra = Extra.ignore


class Metadata(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    locale: Optional[str] = None

    class Config:
        extra = Extra.ignore


class HoneypotRequest(BaseModel):
    # Honeypot fields (OPTIONAL now)
    sessionId: Optional[str] = None
    message: Optional[Message] = None
    conversationHistory: Optional[List[Message]] = []
    metadata: Optional[Metadata] = None

    # GUVI generic fields
    language: Optional[str] = None
    audioFormat: Optional[str] = None
    audioBase64: Optional[str] = None

    class Config:
        extra = Extra.ignore


class HoneypotResponse(BaseModel):
    status: str
    scamDetected: bool
    reply: str
    confidenceScore: float
