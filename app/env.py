import random
from app.models import Observation, Action
from app.tasks import generate_task
from app.grader import grade


class SmartInboxEnv:
    def __init__(self):
        self.task = None
        self.history = []
        self.step_count = 0
        self.max_steps = 5
        self.done = False

    async def reset(self):
        self.task = generate_task()
        self.history = []
        self.step_count = 0
        self.done = False

        return self._get_obs()

    def _get_obs(self):
        email = self.task["email"]

        return {
            "observation": Observation(
                email_id=self.task["id"],
                sender=email["sender"],
                subject=email["subject"],
                body=email["body"],
                history=self.history,
                step_count=self.step_count,
                max_steps=self.max_steps
            ),
            "done": self.done
        }

    async def step(self, action: Action):
        self.step_count += 1

        self.history.append(f"{action.action_type}: {action.content}")

        reward = 0.0

        # intermediate rewards
        if action.action_type == "analyze":
            reward += 0.05

        if action.action_type == "ask":
            reward += 0.05

        # final action
        if action.action_type in ["reply", "ignore"]:
            reward = grade(self.task, action, self.step_count, self.max_steps)
            self.done = True

        if self.step_count >= self.max_steps:
            self.done = True

        return {
            "observation": self._get_obs()["observation"],
            "reward": reward,
            "done": self.done,
            "info": {}
        }

    async def state(self):
        return {
            "task": self.task,
            "history": self.history
        }

    async def close(self):
        pass