from collections.abc import Callable

from .agent import Agent
from .config import Settings
from .llm import LLMClient
from .tools.discord_reply import DiscordReplyTool
from .tools.registry import ToolRegistry
from .tools.student_lookup import StudentLookupTool
from .tools.task_context import TaskContextTool


def build_registry(
    approve: Callable[[str, str], bool],
    send: Callable[[str, str], dict],
) -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(StudentLookupTool())
    registry.register(TaskContextTool())
    registry.register(DiscordReplyTool(approve=approve, send=send))
    return registry


def build_agent(
    settings: Settings,
    approve: Callable[[str, str], bool],
    send: Callable[[str, str], dict],
) -> Agent:
    registry = build_registry(approve, send)
    llm = LLMClient(settings.llm_api_key, settings.llm_model, settings.llm_base_url)
    return Agent(llm, registry, settings)
