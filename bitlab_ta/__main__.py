import json

from .factory import build_registry


def _console_approve(channel: str, text: str) -> bool:
    print(f"\n[approval needed] channel={channel}\n{text}\n")
    return input("send? [y/N] ").strip().lower() == "y"


def _console_send(channel: str, text: str) -> dict:
    print(f"[sent -> {channel}] {text}")
    return {"sent": True, "channel": channel}


def main() -> None:
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


if __name__ == "__main__":
    main()
