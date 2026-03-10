from pydantic_settings import BaseSettings
from typing import List, Optional
import json
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    anthropic_api_key: str
    database_url: Optional[str] = None
    postgres_url: Optional[str] = None  # Vercel Postgres variable
    postgres_url_non_pooling: Optional[str] = None  # Vercel Postgres non-pooling (for migrations)
    postgres_prisma_url: Optional[str] = None  # Vercel Postgres Prisma URL
    cors_origins: str = '["http://localhost:5173"]'
    claude_model: str = "claude-sonnet-4-5"
    max_tokens: int = 4096

    @property
    def db_url(self) -> str:
        """Get database URL from environment variables."""
        # Use POSTGRES_URL (direct connection, better for asyncpg)
        url = self.postgres_url or self.database_url
        if not url:
            return "postgresql+asyncpg://postgres:postgres@localhost:5432/mixdrink_db"
        # Convert postgres:// to postgresql+asyncpg://
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string."""
        return json.loads(self.cors_origins)

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
