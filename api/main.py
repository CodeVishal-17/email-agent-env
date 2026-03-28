from fastapi import FastAPI
from pydantic import BaseModel
from app.env import EmailEnv

app = FastAPI()
env = EmailEnv()

class Action(BaseModel):
    category: str | None = None
    priority: str | None = None
    action_type: str | None = None
    reply: str | None = None

@app.get("/")
def home():
    return {"message": "AI Executive Assistant Environment 🚀"}

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