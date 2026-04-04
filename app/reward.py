def compute_step_reward(correct):
    return 0.3 if correct else -0.2  # stronger penalty

def compute_final_reward(score):
    return score * 1.2  # amplify good behavior