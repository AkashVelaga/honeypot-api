from typing import Dict, List


class SessionData:
    def __init__(self):
        self.total_messages = 0
        self.intelligence = {
            "bankAccounts": [],
            "upiIds": [],
            "phishingLinks": [],
            "phoneNumbers": [],
            "suspiciousKeywords": []
        }
        self.completed = False


SESSION_STORE: Dict[str, SessionData] = {}


def get_session(session_id: str) -> SessionData:
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = SessionData()
    return SESSION_STORE[session_id]


def merge_intelligence(target: dict, new_data: dict):
    for key, values in new_data.items():
        if key in target:
            target[key] = list(set(target[key] + values))
