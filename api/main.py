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

@app.get("/")
def home():
    return {"message": "AI Email RL Environment 🚀"}

# MUST BE POST (validator requirement)
@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    return env.step(action.model_dump())  # ✅ FIXED

@app.get("/state")
def state():
    return env.state() or {}  # ✅ SAFE FIX

@app.get("/tasks")
def tasks():
    return [
        {"id": "easy", "desc": "Classify email"},
        {"id": "medium", "desc": "Classify + priority"},
        {"id": "hard", "desc": "Full decision pipeline"}
    ]

# ================= AUTO AGENT =================

@app.post("/auto")
def auto(email: dict):
    text = email.get("text", "").lower()

    if any(w in text for w in ["free", "offer", "win", "click", "off", "%"]):
        return {
            "category": "spam",
            "priority": "low",
            "action_type": "ignore",
            "reply": ""
        }

    if "meeting" in text:
        return {
            "category": "important",
            "priority": "high",
            "action_type": "schedule",
            "reply": "Confirmed, I will attend the meeting"
        }

    if "interview" in text:
        return {
            "category": "important",
            "priority": "high",
            "action_type": "reply",
            "reply": "Thank you, I will attend the interview"
        }

    if "suspicious" in text or "account" in text:
        return {
            "category": "important",
            "priority": "high",
            "action_type": "escalate",
            "reply": "I will contact support immediately"
        }

    return {
        "category": "important",
        "priority": "low",
        "action_type": "reply",
        "reply": "Noted."
    }