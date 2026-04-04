import asyncio
import os
from typing import List

from my_env_v4 import MyEnvV4Action, MyEnvV4Env

# ================= CONFIG =================

TASK_NAME = "email-agent"
BENCHMARK = "my_env_v4"
MODEL_NAME = "rule-based-agent"

MAX_STEPS = 5

# ================= YOUR AI LOGIC =================

def agent(email: str):
    email = email.lower()

    if any(w in email for w in ["free", "offer", "win", "click", "off"]):
        return "ignore spam email"

    if "meeting" in email:
        return "schedule meeting"

    if "interview" in email:
        return "reply interview confirmation"

    if "suspicious" in email:
        return "escalate security issue"

    return "generic reply"

# ================= LOGGING =================

def log_start():
    print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}", flush=True)

def log_step(step, action, reward, done):
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error=null",
        flush=True,
    )

def log_end(success, steps, score, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )

# ================= MAIN =================

async def main():
    env = await MyEnvV4Env.from_docker_image(os.getenv("IMAGE_NAME"))

    rewards = []
    steps_taken = 0

    log_start()

    try:
        result = await env.reset()
        email = result.observation.echoed_message

        for step in range(1, MAX_STEPS + 1):
            if result.done:
                break

            action_text = agent(email)

            result = await env.step(MyEnvV4Action(message=action_text))

            reward = result.reward or 0.0
            done = result.done

            rewards.append(reward)
            steps_taken = step

            log_step(step, action_text, reward, done)

            email = result.observation.echoed_message

            if done:
                break

        score = min(sum(rewards) / (MAX_STEPS * 10), 1.0)
        success = score > 0.2

    finally:
        await env.close()
        log_end(success, steps_taken, score, rewards)

if __name__ == "__main__":
    asyncio.run(main())
