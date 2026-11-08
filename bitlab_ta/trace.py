import json
import time
from dataclasses import dataclass, field


@dataclass
class Trace:
    goal: str
    events: list = field(default_factory=list)

    def record(self, kind: str, **data) -> None:
        self.events.append({"at": round(time.time(), 3), "kind": kind, **data})

    def as_json(self) -> str:
        return json.dumps(
            {"goal": self.goal, "events": self.events},
            ensure_ascii=False,
            indent=2,
        )
