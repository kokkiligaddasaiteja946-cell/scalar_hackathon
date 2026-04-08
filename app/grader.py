def grade(task, action, step_count, max_steps):
    score = 0.0
    expected = task["expected"]

    # ✅ correctness
    if action.action_type == expected["action_type"]:
        score += 0.3

    if action.priority == expected["priority"]:
        score += 0.2

    # ✅ quality of response
    if action.content:
        content = action.content.lower()

        if any(word in content for word in ["sorry", "apologize"]):
            score += 0.2

        if any(word in content for word in ["schedule", "time", "meeting"]):
            score += 0.1

        if len(content) > 20:
            score += 0.1

    # ✅ efficiency reward
    efficiency = 1 - (step_count / max_steps)
    score += 0.1 * efficiency

    # ❌ penalties
    if step_count >= max_steps:
        score -= 0.2

    return max(0.0, min(score, 1.0))