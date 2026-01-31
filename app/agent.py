import random

def generate_agent_reply(message, history):
    text = message.text.lower()

    # Banking / account scare
    if any(k in text for k in ["account", "bank", "blocked", "suspended", "compromised"]):
        return random.choice([
            "Why is my account being blocked? I didn’t do anything.",
            "This is worrying… which branch is this related to?",
            "I just used my account yesterday. What happened suddenly?",
        ])

    # OTP / verification scam
    if "otp" in text or "verification" in text:
        return random.choice([
            "I’m not very good with these messages. What verification is this?",
            "I got many scam calls earlier… how do I know this is real?",
            "Is this required right now? I’m a bit confused.",
        ])

    # UPI / payment bait
    if "upi" in text or "payment" in text:
        return random.choice([
            "I don’t usually share UPI details. Why is it needed?",
            "Can this be done through the bank branch instead?",
            "I’m outside right now, is there another way?",
        ])

    # Escalation fallback
    return random.choice([
        "Can you explain once more? I’m not understanding properly.",
        "Sorry, I’m a bit nervous about this.",
        "Please tell me slowly, I’m not familiar with these things.",
    ])
