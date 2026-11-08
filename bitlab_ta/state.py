from dataclasses import dataclass, field
from enum import Enum


class Status(str, Enum):
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


@dataclass
class AgentState:
    goal: str
    question: str
    status: Status = Status.RUNNING
    steps: int = 0
    tool_calls: int = 0
    context: dict = field(default_factory=dict)
    draft_answer: str = ""
    stop_reason: str = ""
