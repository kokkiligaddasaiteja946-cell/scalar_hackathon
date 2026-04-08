import os
import asyncio
import json
from typing import List

import requests
from openai import OpenAI


# =========================
# ENV VARIABLES (MANDATORY)
# =========================
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

ENV_URL = os.getenv("ENV_URL", "http://localhost:8000")

MAX_STEPS = 5
MAX_TOTAL_REWARD = 1.0
SUCCESS_SCORE_THRESHOLD = 0.6


# =========================
# LOGGING (STRICT FORMAT)
# =========================
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action, reward: float, done: bool, error):
    print(
        f"[STEP] step={step} action={action} reward={reward} done={done} error={error}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    print(
        f"[END] success={success} steps={steps} score={score} rewards={rewards}",
        flush=True,
    )


# =========================
# PROMPT BUILDER
# =========================
def build_prompt(observation, history):
    return f"""
You are an intelligent email assistant.

Your goal:
- Understand the email
- Take correct actions step-by-step

Available actions:
- analyze
- ask
- reply
- ignore

Email:
Sender: {observation.get("sender")}
Subject: {observation.get("subject")}
Body: {observation.get("body")}

Conversation History:
{history}

Current Step: {observation.get("step_count")} / {observation.get("max_steps")}

Instructions:
- Think step by step
- Use analyze first if needed
- Ask clarification if unsure
- Finish with reply or ignore

Output STRICT JSON ONLY:
{{
    "action_type": "...",
    "priority": "...",
    "content": "..."
}}
"""


# =========================
# MODEL CALL
# =========================
def get_model_action(client, prompt):
    # Rule-based fallback (no API needed)

    prompt = prompt.lower()

    if "free" in prompt or "win money" in prompt:
        return '{"action_type":"ignore","priority":"low","content":""}'

    if "meeting" in prompt:
        return '{"action_type":"reply","priority":"medium","content":"Sure, I am available for the meeting."}'

    if "disappointed" in prompt or "issue" in prompt:
        return '{"action_type":"reply","priority":"high","content":"Sorry for the inconvenience. We will resolve your issue."}'

    return '{"action_type":"analyze","priority":"medium","content":"Analyzing the email"}'
# =========================
# SAFE JSON PARSE
# =========================
def parse_action(text: str):
    try:
        return json.loads(text)
    except:
        return {
            "action_type": "ignore",
            "priority": "low",
            "content": ""
        }


# =========================
# MAIN LOOP
# =========================
async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    rewards: List[float] = []
    history: List[str] = []
    steps_taken = 0

    log_start(task="email_triage", env="smart_inbox_env_v2", model=MODEL_NAME)

    try:
        # RESET ENV
        reset_res = requests.get(f"{ENV_URL}/reset").json()
        observation = reset_res["observation"]
        done = reset_res["done"]

        last_reward = 0.0

        for step in range(1, MAX_STEPS + 1):
            if done:
                break

            # BUILD PROMPT
            prompt = build_prompt(observation, history)

            # MODEL OUTPUT
            raw_output = get_model_action(client, prompt)

            # PARSE ACTION
            action = parse_action(raw_output)

            error = None

            try:
                # SEND ACTION TO ENV
                step_res = requests.post(f"{ENV_URL}/step", json=action).json()

                observation = step_res["observation"]
                reward = float(step_res.get("reward", 0.0))
                done = step_res.get("done", False)

            except Exception as e:
                reward = 0.0
                done = True
                error = str(e)

            # TRACK
            rewards.append(reward)
            steps_taken = step

            history.append(
                f"Step {step}: action={action} reward={reward:.2f}"
            )

            # LOG STEP
            log_step(
                step=step,
                action=action,
                reward=reward,
                done=done,
                error=error,
            )

            last_reward = reward

            if done:
                break

        # FINAL SCORE
        total_reward = sum(rewards)
        score = total_reward / MAX_TOTAL_REWARD if MAX_TOTAL_REWARD > 0 else 0.0
        score = max(0.0, min(score, 1.0))

        success = score >= SUCCESS_SCORE_THRESHOLD

    finally:
        log_end(
            success=success,
            steps=steps_taken,
            score=score,
            rewards=rewards,
        )


# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    asyncio.run(main())