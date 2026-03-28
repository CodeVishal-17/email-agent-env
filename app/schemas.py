from pydantic import BaseModel

class Observation(BaseModel):
    email_id: int
    email_text: str

class Action(BaseModel):
    category: str
    priority: str
    reply: str