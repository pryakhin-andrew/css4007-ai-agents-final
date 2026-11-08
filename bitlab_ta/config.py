import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    llm_api_key: str
    llm_model: str
    llm_base_url: str
    discord_bot_token: str
    approver_discord_id: str
    google_service_account_file: str
    students_sheet_id: str
    bitlab_api_base: str
    bitlab_api_token: str
    max_steps: int
    max_tool_calls: int
    max_retries: int

    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            llm_api_key=os.getenv("LLM_API_KEY", ""),
            llm_model=os.getenv("LLM_MODEL", "openai/gpt-4o-mini"),
            llm_base_url=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
            discord_bot_token=os.getenv("DISCORD_BOT_TOKEN", ""),
            approver_discord_id=os.getenv("APPROVER_DISCORD_ID", ""),
            google_service_account_file=os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", ""),
            students_sheet_id=os.getenv("STUDENTS_SHEET_ID", ""),
            bitlab_api_base=os.getenv("BITLAB_API_BASE", ""),
            bitlab_api_token=os.getenv("BITLAB_API_TOKEN", ""),
            max_steps=int(os.getenv("AGENT_MAX_STEPS", "8")),
            max_tool_calls=int(os.getenv("AGENT_MAX_TOOL_CALLS", "12")),
            max_retries=int(os.getenv("AGENT_MAX_RETRIES", "2")),
        )
