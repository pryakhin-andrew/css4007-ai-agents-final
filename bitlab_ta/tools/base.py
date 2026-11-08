from abc import ABC, abstractmethod


class Tool(ABC):
    name: str = ""
    description: str = ""
    permission: str = "read"

    @abstractmethod
    def schema(self) -> dict:
        ...

    @abstractmethod
    def validate(self, args: dict) -> dict:
        ...

    @abstractmethod
    def run(self, args: dict) -> dict:
        ...
