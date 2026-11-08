from .base import Tool
from ..guardrails import require

# Mock task catalog for Week 10. Replaced by the Bitlab portal API in Week 13.
_MOCK_TASKS = {
    "task-05-rest": {
        "title": "Build a REST controller",
        "requirements": [
            "Expose GET and POST endpoints for a Note resource",
            "Validate the request body",
            "Return proper HTTP status codes",
        ],
        "deadline": "2026-11-20",
    },
    "task-07-auth": {
        "title": "JWT authentication",
        "requirements": [
            "Issue a JWT on login",
            "Protect endpoints with a security filter",
            "Reject expired or invalid tokens",
        ],
        "deadline": "2026-11-27",
    },
}


class TaskContextTool(Tool):
    name = "get_task_context"
    description = (
        "Fetch a Bitlab task's title, requirements and deadline by its id, "
        "so answers are grounded in the real assignment. Read-only."
    )
    permission = "read"

    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "Task id, for example task-07-auth"}
                    },
                    "required": ["task_id"],
                },
            },
        }

    def validate(self, args: dict) -> dict:
        return {"task_id": require("task_id", args.get("task_id", "")).lower()}

    def run(self, args: dict) -> dict:
        task = _MOCK_TASKS.get(args["task_id"])
        if not task:
            return {"found": False, "error": "task_not_found"}
        return {"found": True, "task": task}
