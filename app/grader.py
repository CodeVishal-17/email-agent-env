from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once (important)
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(a, b):
    emb1 = model.encode([a])
    emb2 = model.encode([b])
    return cosine_similarity(emb1, emb2)[0][0]

def grade_action(memory, expected):
    score = 0

    # Category
    if memory.get("category") == expected["category"]:
        score += 0.3

    # Priority
    if memory.get("priority") == expected["priority"]:
        score += 0.3

    # Reply (SMART PART 🔥)
    reply = memory.get("reply", "")
    expected_reply = expected["expected_reply"]

    if expected_reply.strip() == "":
        similarity = 1.0  # spam case, no reply needed
    else:
        similarity = semantic_similarity(reply, expected_reply)

    # scale reply score
    if similarity > 0.7:
        score += 0.4
    elif similarity > 0.5:
        score += 0.2
    else:
        score += 0

    return min(score, 1.0)