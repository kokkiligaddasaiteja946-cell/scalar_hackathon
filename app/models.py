from pydantic import BaseModel
from typing import Optional, List


class Observation(BaseModel):
    email_id: str
    sender: str
    subject: str
    body: str
    history: List[str]
    step_count: int
    max_steps: int


class Action(BaseModel):
    action_type: str  # "analyze", "ask", "reply", "ignore"
    content: Optional[str]
    priority: Optional[str]

class Reward(BaseModel):
    score: float