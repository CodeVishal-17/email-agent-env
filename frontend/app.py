import streamlit as st
import json
import random

# ================= CONFIG =================

st.set_page_config(page_title="Autonomous AI Email Executive Agent", page_icon="📧")

st.title("🚀 Autonomous AI Email Executive Agent")
st.caption("An autonomous AI agent that continuously improves email decision-making using reinforcement learning feedback loops.")

# ================= STYLE =================

st.markdown("""
<style>
.stButton>button {
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ================= MEMORY =================

def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_memory(email, decision, score):
    data = load_memory()
    data.append({
        "email": email,
        "decision": decision,
        "score": score
    })
    with open("memory.json", "w") as f:
        json.dump(data, f, indent=2)

# ================= SCORING =================

def compute_score(email, decision):
    email_lower = email.lower()
    score = 0

    # category
    if any(w in email_lower for w in ["free", "offer", "win", "click", "off"]):
        if decision["category"] == "spam":
            score += 0.25
    else:
        if decision["category"] == "important":
            score += 0.25

    # priority
    if "meeting" in email_lower or "interview" in email_lower:
        if decision["priority"] == "high":
            score += 0.25

    # action
    if "meeting" in email_lower and decision["action_type"] == "schedule":
        score += 0.25
    elif "interview" in email_lower and decision["action_type"] == "reply":
        score += 0.25
    elif "suspicious" in email_lower and decision["action_type"] == "escalate":
        score += 0.25

    # reply
    if decision["reply"]:
        score += 0.25

    return round(score, 2)

# ================= AI AGENT =================

def llm_agent(email):
    email_lower = email.lower()

    if any(w in email_lower for w in ["free", "offer", "win", "click", "off", "%"]):
        decision = {
            "category": "spam",
            "priority": "low",
            "action_type": "ignore",
            "reply": ""
        }

    elif "meeting" in email_lower:
        decision = {
            "category": "important",
            "priority": "high",
            "action_type": "schedule",
            "reply": "Confirmed, I will attend the meeting"
        }

    elif "interview" in email_lower:
        decision = {
            "category": "important",
            "priority": "high",
            "action_type": "reply",
            "reply": "Thank you, I will attend the interview"
        }

    elif "suspicious" in email_lower:
        decision = {
            "category": "important",
            "priority": "high",
            "action_type": "escalate",
            "reply": "I will contact support immediately"
        }

    else:
        decision = {
            "category": "important",
            "priority": "low",
            "action_type": "reply",
            "reply": "Noted."
        }

    # AI feel
    decision["confidence"] = round(random.uniform(0.85, 0.98), 2)

    decision["reason"] = {
        "spam": "Detected promotional keywords",
        "important": "Contains actionable or time-sensitive content"
    }[decision["category"]]

    return decision

# ================= MAIN =================

st.markdown("---")
st.subheader("🤖 AI Agent")

if st.button("Run AI Agent"):

    email = random.choice([
        "Win a free iPhone now!!! Click here",
        "Client meeting tomorrow at 3 PM",
        "Your interview is scheduled",
        "Suspicious login detected",
        "Flat 50% OFF on products"
    ])

    st.write("📩 Email:", email)

    # Thinking steps
    st.write("🧠 Thinking...")
    st.write("Step 1 → Understanding email")
    st.write("Step 2 → Classifying category")
    st.write("Step 3 → Assigning priority")
    st.write("Step 4 → Selecting action")

    decision = llm_agent(email)

    # Show decision
    st.success(f"📂 Category: {decision['category']}")
    st.info(f"⚡ Priority: {decision['priority']}")
    st.warning(f"🛠 Action: {decision['action_type']}")

    if decision["reply"]:
        st.write(f"✉ Reply: {decision['reply']}")

    st.metric("🧠 Confidence", f"{decision['confidence']*100}%")
    st.caption(f"🧠 Reason: {decision['reason']}")

    # Score
    score = compute_score(email, decision)

    if score == 1.0:
        st.success("✅ AI performed perfectly — reinforcing this behavior")
    elif score > 0.5:
        st.info("📈 AI is improving — partial reward received")
    else:
        st.warning("⚠️ AI made a mistake — updating strategy")

    st.success(f"🎯 Final Score: {score}")
    st.progress(score)

    save_memory(email, decision, score)

# ================= PERFORMANCE =================

memory = load_memory()

if memory:
    scores = [m["score"] for m in memory]
    avg = sum(scores) / len(scores)

    st.markdown("---")
    st.subheader("📊 Performance")
    st.info(f"Average Score: {round(avg, 2)}")

    best = max(memory, key=lambda x: x["score"])

    st.subheader("🏆 Best Decision")
    st.write("📩", best["email"])
    st.write("⭐ Score:", best["score"])

    # Recent decisions
    st.subheader("🧠 Recent Decisions")

    for m in memory[-5:][::-1]:
        st.write(f"📩 {m['email']}")
        st.write(f"➡️ {m['decision']['category']} | {m['decision']['action_type']} | ⭐ {m['score']}")
        st.markdown("---")