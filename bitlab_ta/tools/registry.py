from .base import Tool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name]

    def schemas(self) -> list[dict]:
        return [tool.schema() for tool in self._tools.values()]

    def dispatch(self, name: str, args: dict) -> dict:
        tool = self.get(name)
        validated = tool.validate(args)
        return tool.run(validated)
