from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    anthropic_api_key: str
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/mixdrink_db"
    cors_origins: str = '["http://localhost:5173"]'
    claude_model: str = "claude-sonnet-4-5"
    max_tokens: int = 4096

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string."""
        return json.loads(self.cors_origins)

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
