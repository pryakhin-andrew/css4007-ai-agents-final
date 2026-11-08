from collections.abc import Callable

from .base import Tool
from ..guardrails import require


class DiscordReplyTool(Tool):
    name = "send_reply"
    description = (
        "Send a reply to the student in Discord. Consequential action: "
        "it is held for human approval before anything is sent."
    )
    permission = "write"

    def __init__(
        self,
        approve: Callable[[str, str], bool],
        send: Callable[[str, str], dict],
    ) -> None:
        self._approve = approve
        self._send = send

    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "channel": {"type": "string", "description": "Discord channel or user id"},
                        "text": {"type": "string", "description": "The reply to send"},
                    },
                    "required": ["channel", "text"],
                },
            },
        }

    def validate(self, args: dict) -> dict:
        return {
            "channel": require("channel", args.get("channel", "")),
            "text": require("text", args.get("text", "")),
        }

    def run(self, args: dict) -> dict:
        if not self._approve(args["channel"], args["text"]):
            return {"sent": False, "reason": "approval_denied"}
        return self._send(args["channel"], args["text"])
