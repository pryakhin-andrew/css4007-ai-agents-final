import unittest

from bitlab_ta.guardrails import GuardrailError
from bitlab_ta.tools.discord_reply import DiscordReplyTool
from bitlab_ta.tools.student_lookup import StudentLookupTool
from bitlab_ta.tools.task_context import TaskContextTool


class StudentLookupTests(unittest.TestCase):
    def test_found(self):
        tool = StudentLookupTool()
        result = tool.run(tool.validate({"query": "Arman"}))
        self.assertTrue(result["found"])
        self.assertEqual(result["student"]["group"], "BE-2")

    def test_not_found(self):
        tool = StudentLookupTool()
        result = tool.run(tool.validate({"query": "nobody"}))
        self.assertFalse(result["found"])
        self.assertEqual(result["error"], "student_not_found")

    def test_validate_rejects_empty(self):
        with self.assertRaises(GuardrailError):
            StudentLookupTool().validate({"query": ""})


class TaskContextTests(unittest.TestCase):
    def test_found(self):
        tool = TaskContextTool()
        result = tool.run(tool.validate({"task_id": "task-07-auth"}))
        self.assertTrue(result["found"])
        self.assertIn("deadline", result["task"])

    def test_not_found(self):
        tool = TaskContextTool()
        result = tool.run(tool.validate({"task_id": "task-99"}))
        self.assertFalse(result["found"])


class DiscordReplyTests(unittest.TestCase):
    def test_requires_approval(self):
        sent = []
        tool = DiscordReplyTool(
            approve=lambda channel, text: False,
            send=lambda channel, text: sent.append((channel, text)),
        )
        result = tool.run(tool.validate({"channel": "123", "text": "hi"}))
        self.assertFalse(result["sent"])
        self.assertEqual(result["reason"], "approval_denied")
        self.assertEqual(sent, [])

    def test_sends_after_approval(self):
        tool = DiscordReplyTool(
            approve=lambda channel, text: True,
            send=lambda channel, text: {"sent": True, "channel": channel},
        )
        result = tool.run(tool.validate({"channel": "123", "text": "hi"}))
        self.assertTrue(result["sent"])


if __name__ == "__main__":
    unittest.main()
