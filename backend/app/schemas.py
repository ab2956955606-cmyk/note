from typing import Any

from pydantic import BaseModel, Field


class GoalRequest(BaseModel):
    goal: str = ""
    deadline: str = ""
    daily_hours: float = 2
    context: str = ""
    date: str = ""
    plans: dict[str, Any] = Field(default_factory=dict)


class ReviewRequest(BaseModel):
    goal: str = ""
    context: str = ""
    date: str = ""
    plans: dict[str, Any] = Field(default_factory=dict)


class RagRequest(BaseModel):
    goal: str = ""
    context: str = ""
    date: str = ""
    plans: dict[str, Any] = Field(default_factory=dict)
