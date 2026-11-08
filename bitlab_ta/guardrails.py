import re

INJECTION_PATTERNS = [
    r"ignore (all |previous |the )?(instructions|rules)",
    r"disregard .*(instructions|rules)",
    r"system prompt",
    r"reveal .*(prompt|key|token|password)",
    r"send .* to (everyone|all students|the group)",
    r"(give|show) me .*(answer key|solution|the answers)",
]


class GuardrailError(Exception):
    pass


def require(name: str, value: str) -> str:
    if not value or not value.strip():
        raise GuardrailError(f"{name} is required")
    return value.strip()


def looks_like_injection(untrusted_text: str) -> bool:
    text = untrusted_text.lower()
    return any(re.search(pattern, text) for pattern in INJECTION_PATTERNS)


def within_limits(steps: int, tool_calls: int, max_steps: int, max_tool_calls: int) -> bool:
    return steps < max_steps and tool_calls < max_tool_calls
