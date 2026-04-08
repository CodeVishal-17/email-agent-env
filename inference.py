import requests

BASE_URL = "http://localhost:7860"

def log_start():
    print("[START] task=email-agent env=custom model=rule-based", flush=True)

def log_step(step, action, reward, done):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null", flush=True)

def log_end(success, steps, score, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)


def agent(email):
    email = email.lower()

    if "free" in email or "win" in email:
        return {"category": "spam", "priority": "low", "action_type": "ignore", "reply": ""}

    if "meeting" in email:
        return {"category": "important", "priority": "high", "action_type": "schedule", "reply": "Confirmed"}

    if "interview" in email:
        return {"category": "important", "priority": "high", "action_type": "reply", "reply": "I will attend"}

    return {"category": "important", "priority": "low", "action_type": "reply", "reply": "Noted"}


def main():
    rewards = []
    steps = 0

    log_start()

    # RESET
    res = requests.post(f"{BASE_URL}/reset").json()
    email = res["email_text"]

    decision = agent(email)

    # STEP 1
    r1 = requests.post(f"{BASE_URL}/step", json={"category": decision["category"]}).json()
    log_step(1, decision["category"], r1.get("reward", 0), False)

    # STEP 2
    r2 = requests.post(f"{BASE_URL}/step", json={"priority": decision["priority"]}).json()
    log_step(2, decision["priority"], r2.get("reward", 0), False)

    # STEP 3
    r3 = requests.post(f"{BASE_URL}/step", json={"action_type": decision["action_type"]}).json()
    log_step(3, decision["action_type"], r3.get("reward", 0), False)

    # STEP 4
    r4 = requests.post(f"{BASE_URL}/step", json={"reply": decision["reply"]}).json()
    log_step(4, decision["reply"], r4.get("reward", 0), True)

    rewards = [
        r1.get("reward", 0),
        r2.get("reward", 0),
        r3.get("reward", 0),
        r4.get("reward", 0),
    ]

    score = min(sum(rewards), 1.0)
    success = score > 0.3

    log_end(success, 4, score, rewards)


if __name__ == "__main__":
    main()