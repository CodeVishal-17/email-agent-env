import random
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ============================
# MODEL
# ============================
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(a, b):
    emb1 = model.encode([a])
    emb2 = model.encode([b])
    return cosine_similarity(emb1, emb2)[0][0]

# ============================
# GRADER
# ============================
def grade_action(memory, expected):
    score = 0

    if memory.get("category") == expected["category"]:
        score += 0.25

    if memory.get("priority") == expected["priority"]:
        score += 0.25

    if memory.get("action_type") == expected["expected_action"]:
        score += 0.25
    else:
        score -= 0.2

    reply = memory.get("reply", "")
    expected_reply = expected["expected_reply"]

    if expected_reply.strip() == "":
        similarity = 1.0
    else:
        similarity = semantic_similarity(reply, expected_reply)

    if similarity > 0.7:
        score += 0.25
    elif similarity > 0.5:
        score += 0.15

    return max(0.0, min(score, 1.0))

# ============================
# REWARD
# ============================
def compute_step_reward(correct):
    return 0.3 if correct else -0.2

# ============================
# ENVIRONMENT
# ============================
class EmailEnv:
    def __init__(self):
        self.emails = [
            {
                "text": "Win a free iPhone now!!! Click here",
                "category": "spam",
                "priority": "low",
                "expected_action": "ignore",
                "expected_reply": ""
            },
            {
                "text": "Your job interview is scheduled tomorrow at 10 AM",
                "category": "important",
                "priority": "high",
                "expected_action": "reply",
                "expected_reply": "Thank you, I will attend the interview"
            },
            {
                "text": "Client meeting tomorrow at 3 PM. Please confirm.",
                "category": "important",
                "priority": "high",
                "expected_action": "schedule",
                "expected_reply": "Confirmed, I will attend the meeting"
            },
            {
                "text": "Your account has suspicious activity, contact support immediately",
                "category": "important",
                "priority": "high",
                "expected_action": "escalate",
                "expected_reply": "I will contact support immediately"
            }
        ]

        self.current = None
        self.stage = 0
        self.memory = {}

    def reset(self):
        self.current = random.choice(self.emails)
        self.stage = 0
        self.memory = {}

        return {
            "stage": "classify",
            "email_text": self.current["text"]
        }
    def step(self, action):
    
        if self.current is None:
            return {"error": "Call /reset first"}

        if self.stage == 0 and "category" not in action:
            return {"error": "Expected 'category'"}

        if self.stage == 1 and "priority" not in action:
            return {"error": "Expected 'priority'"}

        if self.stage == 2 and "action_type" not in action:
            return {"error": "Expected 'action_type'"}

        if self.stage == 3 and "reply" not in action:
            return {"error": "Expected 'reply'"}

        # ============================
        # STEP 1: CATEGORY
        # ============================
        if self.stage == 0:
            correct = action["category"] == self.current["category"]
            reward = compute_step_reward(correct)

            self.memory["category"] = action["category"]
            self.stage = 1

            return {"stage": "priority", "reward": reward, "done": False}

        # ============================
        # STEP 2: PRIORITY
        # ============================
        elif self.stage == 1:
            correct = action["priority"] == self.current["priority"]
            reward = compute_step_reward(correct)

            self.memory["priority"] = action["priority"]
            self.stage = 2

            return {"stage": "action", "reward": reward, "done": False}

        # ============================
        # STEP 3: ACTION
        # ============================
        elif self.stage == 2:
            correct = action["action_type"] == self.current["expected_action"]
            reward = compute_step_reward(correct)

            self.memory["action_type"] = action["action_type"]
            self.stage = 3

            return {"stage": "reply", "reward": reward, "done": False}

        # ============================
        # STEP 4: REPLY
        # ============================
        elif self.stage == 3:
            self.memory["reply"] = action["reply"]

            final_score = grade_action(self.memory, self.current)

            self.stage = 4

            return {
                "stage": "done",
                "reward": final_score,
                "done": True,
                "final_score": final_score,
                "memory": self.memory,
                "explanation": "Score based on category, priority, action, and semantic reply match"
            }

    def state(self):
        return {
            "stage": self.stage,
            "memory": self.memory,
            "email": self.current
        }

# ============================
# API
# ============================
app = FastAPI()
env = EmailEnv()

@app.get("/")
def home():
    return {"message": "AI Executive Assistant Environment 🚀"}

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: dict):
    return env.step(action)

@app.get("/state")
def state():
    return env.state()