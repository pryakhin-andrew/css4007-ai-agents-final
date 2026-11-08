from .base import Tool
from ..guardrails import require

# Mock roster for Week 10. Replaced by the Google Sheets API in Week 13.
_MOCK_STUDENTS = {
    "arman": {"name": "Arman S.", "group": "BE-2", "current_task": "task-07-auth", "completed": 6, "total": 12},
    "dana": {"name": "Dana K.", "group": "BE-1", "current_task": "task-05-rest", "completed": 4, "total": 12},
}


class StudentLookupTool(Tool):
    name = "lookup_student"
    description = (
        "Look up a Bitlab student's record (group, current task, progress) "
        "by their name or Discord handle. Read-only."
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
                        "query": {"type": "string", "description": "Student name or Discord handle"}
                    },
                    "required": ["query"],
                },
            },
        }

    def validate(self, args: dict) -> dict:
        return {"query": require("query", args.get("query", "")).lower()}

    def run(self, args: dict) -> dict:
        record = _MOCK_STUDENTS.get(args["query"])
        if not record:
            return {"found": False, "error": "student_not_found"}
        return {"found": True, "student": record}
