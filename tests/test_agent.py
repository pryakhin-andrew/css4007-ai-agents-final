import unittest

from bitlab_ta.agent import Agent
from bitlab_ta.config import Settings
from bitlab_ta.factory import build_registry
from bitlab_ta.llm import LLMResponse, ToolCall


def _settings(**overrides) -> Settings:
    base = dict(
        llm_api_key="x",
        llm_model="m",
        llm_base_url="u",
        discord_bot_token="",
        approver_discord_id="",
        google_service_account_file="",
        students_sheet_id="",
        bitlab_api_base="",
        bitlab_api_token="",
        max_steps=8,
        max_tool_calls=12,
        max_retries=2,
    )
    base.update(overrides)
    return Settings(**base)


class FakeLLM:
    def __init__(self, responses):
        self._responses = list(responses)

    def complete(self, messages, tools):
        return self._responses.pop(0)


def _registry():
    return build_registry(approve=lambda channel, text: True, send=lambda channel, text: {"sent": True})


class AgentTests(unittest.TestCase):
    def test_tool_then_answer(self):
        llm = FakeLLM([
            LLMResponse(tool_calls=[ToolCall(id="1", name="get_task_context", arguments={"task_id": "task-07-auth"})]),
            LLMResponse(text="It needs JWT auth, due 2026-11-27."),
        ])
        state = Agent(llm, _registry(), _settings()).run("When is task-07-auth due?")
        self.assertEqual(state.status.value, "completed")
        self.assertEqual(state.stop_reason, "answer_ready")
        self.assertEqual(state.tool_calls, 1)
        self.assertIn("get_task_context", state.context)

    def test_execution_limit(self):
        looping = [
            LLMResponse(tool_calls=[ToolCall(id="1", name="get_task_context", arguments={"task_id": "task-07-auth"})])
            for _ in range(20)
        ]
        state = Agent(FakeLLM(looping), _registry(), _settings(max_steps=3)).run("loop please")
        self.assertEqual(state.status.value, "stopped")
        self.assertEqual(state.stop_reason, "execution_limit_reached")

    def test_invalid_question(self):
        state = Agent(FakeLLM([]), _registry(), _settings()).run("   ")
        self.assertEqual(state.status.value, "failed")
        self.assertEqual(state.stop_reason, "invalid_question")

    def test_empty_answer_fails(self):
        state = Agent(FakeLLM([LLMResponse(text="   ")]), _registry(), _settings()).run("hi")
        self.assertEqual(state.status.value, "failed")
        self.assertEqual(state.stop_reason, "empty_answer")

    def test_failed_tool_does_not_crash(self):
        llm = FakeLLM([
            LLMResponse(tool_calls=[ToolCall(id="1", name="missing_tool", arguments={})]),
            LLMResponse(text="Sorry, I could not look that up."),
        ])
        state = Agent(llm, _registry(), _settings()).run("use a broken tool")
        self.assertEqual(state.status.value, "completed")
        self.assertEqual(state.context["missing_tool"]["error"], "tool_failed")


if __name__ == "__main__":
    unittest.main()
