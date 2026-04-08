import random

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
                "text": "Your interview is scheduled tomorrow",
                "category": "important",
                "priority": "high",
                "expected_action": "reply",
                "expected_reply": "Thank you, I will attend the interview"
            },
            {
                "text": "Client meeting tomorrow at 3 PM",
                "category": "important",
                "priority": "high",
                "expected_action": "schedule",
                "expected_reply": "Confirmed, I will attend the meeting"
            },
            {
                "text": "Suspicious login detected in your account",
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
            "email_text": self.current["text"]
        }

    def step(self, action):
        if self.current is None:
            return {"error": "Call /reset first"}

        reward = 0.0

        if "category" in action:
            reward += 0.25 if action["category"] == self.current["category"] else 0

        if "priority" in action:
            reward += 0.25 if action["priority"] == self.current["priority"] else 0

        if "action_type" in action:
            reward += 0.25 if action["action_type"] == self.current["expected_action"] else 0

        if "reply" in action:
            reward += 0.25

        return {
            "reward": reward,
            "done": True
        }

    def state(self):
        return {
            "email": self.current
        }