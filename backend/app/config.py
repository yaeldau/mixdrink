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
        # Prefer POSTGRES_PRISMA_URL (connection pooling) for Vercel
        url = self.postgres_prisma_url or self.postgres_url or self.database_url
        if not url:
            return "postgresql+asyncpg://postgres:postgres@localhost:5432/mixdrink_db"
        # Convert postgres:// to postgresql+asyncpg://
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        # Add pgbouncer=true for pooling if using POSTGRES_PRISMA_URL
        if self.postgres_prisma_url and "pgbouncer=true" not in url:
            url += "?pgbouncer=true" if "?" not in url else "&pgbouncer=true"
        return url

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string."""
        return json.loads(self.cors_origins)

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
