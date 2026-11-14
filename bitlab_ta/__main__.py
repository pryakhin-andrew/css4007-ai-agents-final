import json
import sys

from .config import Settings
from .factory import build_agent, build_registry


def _console_approve(channel: str, text: str) -> bool:
    print(f"\n[approval needed] channel={channel}\n{text}\n")
    try:
        return input("send? [y/N] ").strip().lower() == "y"
    except EOFError:
        return False


def _console_send(channel: str, text: str) -> dict:
    print(f"[sent -> {channel}] {text}")
    return {"sent": True, "channel": channel}


def _load_env() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass


def run_demo() -> None:
    registry = build_registry(approve=_console_approve, send=_console_send)

    print("Registered tools:")
    for schema in registry.schemas():
        function = schema["function"]
        print(f"  - {function['name']}: {function['description']}")

    print("\nDemo lookup_student('arman'):")
    print(json.dumps(registry.dispatch("lookup_student", {"query": "arman"}), ensure_ascii=False, indent=2))

    print("\nDemo get_task_context('task-07-auth'):")
    print(json.dumps(registry.dispatch("get_task_context", {"task_id": "task-07-auth"}), ensure_ascii=False, indent=2))

    print("\nDemo unknown student (failure path):")
    print(json.dumps(registry.dispatch("lookup_student", {"query": "nobody"}), ensure_ascii=False, indent=2))


def run_agent(question: str) -> None:
    _load_env()
    settings = Settings.from_env()
    if not settings.llm_api_key:
        print("LLM_API_KEY is not set. Fill it in .env first.")
        return

    agent = build_agent(settings, approve=_console_approve, send=_console_send)
    state = agent.run(question)

    print("\n--- answer ---")
    print(state.draft_answer or "(no answer produced)")
    print(f"\nstatus={state.status.value} steps={state.steps} "
          f"tool_calls={state.tool_calls} stop={state.stop_reason}")
    if agent.trace:
        print("\n--- trace ---")
        print(agent.trace.as_json())


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] == "--demo":
        run_demo()
    else:
        run_agent(" ".join(args))


if __name__ == "__main__":
    main()
