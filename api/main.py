import json
import os
import random
from fastapi import FastAPI
from fastapi import FastAPI
from pydantic import BaseModel
from app.env import EmailEnv

app = FastAPI()
env = EmailEnv()

# ================= MODEL =================

class Action(BaseModel):
    category: str | None = None
    priority: str | None = None
    action_type: str | None = None
    reply: str | None = None

# ================= ROUTES =================

app = FastAPI()

emails = [
    "Win a free iPhone now!!! Click here",
    "Client meeting tomorrow at 3 PM",
    "Your interview is scheduled",
    "Suspicious login detected",
    "Flat 50% OFF on products"
]


def load_emails():
    try:
        path = os.path.join("data", "emails.json")
        with open(path, "r") as f:
            return json.load(f)
    except:
        return [
            "Win a free iPhone now!!! Click here",
            "Client meeting tomorrow at 3 PM",
            "Your interview is scheduled",
            "Suspicious login detected",
            "Flat 50% OFF on products"
        ]


@app.post("/reset")
def reset():
    return {"email_text": random.choice(emails)}

@app.get("/")
def home():
    return {"message": "API running"}

@app.get("/")
def home():
    return {"message": "AI Email RL Environment 🚀"}

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    return env.step(action.dict())

@app.get("/state")
def state():
    return env.state()

@app.get("/tasks")
def tasks():
    return [
        {"id": "easy", "desc": "Classify email"},
        {"id": "medium", "desc": "Classify + priority"},
        {"id": "hard", "desc": "Full decision pipeline"}
    ]

# ================= AUTO AGENT (IMPORTANT) =================

@app.post("/auto")
def auto(email: dict):
    text = email["text"].lower()

    # SPAM
    if any(w in text for w in ["free", "offer", "win", "click", "off", "%"]):
        return {
            "category": "spam",
            "priority": "low",
            "action_type": "ignore",
            "reply": "",
            "confidence": 0.95,
            "reason": "Detected spam/promotional keywords"
        }

    # MEETING
    if "meeting" in text:
        return {
            "category": "important",
            "priority": "high",
            "action_type": "schedule",
            "reply": "Confirmed, I will attend the meeting",
            "confidence": 0.93,
            "reason": "Meeting detected"
        }

    # INTERVIEW
    if "interview" in text:
        return {
            "category": "important",
            "priority": "high",
            "action_type": "reply",
            "reply": "Thank you, I will attend the interview",
            "confidence": 0.92,
            "reason": "Interview detected"
        }

    # SECURITY
    if "suspicious" in text or "account" in text:
        return {
            "category": "important",
            "priority": "high",
            "action_type": "escalate",
            "reply": "I will contact support immediately",
            "confidence": 0.96,
            "reason": "Security issue detected"
        }

    # DEFAULT
    return {
        "category": "important",
        "priority": "low",
        "action_type": "reply",
        "reply": "Noted.",
        "confidence": 0.75,
        "reason": "Default decision"
    }

