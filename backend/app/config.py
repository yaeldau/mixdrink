from pydantic_settings import BaseSettings
from typing import List, Optional
import json
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


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
        # Use POSTGRES_URL_NON_POOLING to bypass pgbouncer (avoids prepared statement issues)
        # Fall back to POSTGRES_URL if non-pooling URL is not available
        url = self.postgres_url_non_pooling or self.postgres_url or self.database_url
        if not url:
            return "postgresql+asyncpg://postgres:postgres@localhost:5432/mixdrink_db"

        # Convert postgres:// to postgresql+asyncpg://
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Parse URL and remove Vercel-specific query parameters
        parsed = urlparse(url)
        if parsed.query:
            # Parse query string
            query_params = parse_qs(parsed.query)
            # Remove all Vercel-specific parameters (asyncpg doesn't support them)
            vercel_params = ['sslmode', 'supa', 'pgbouncer', 'connection_limit']
            for param in vercel_params:
                query_params.pop(param, None)
            # Rebuild query string (will be empty if all params removed)
            new_query = urlencode(query_params, doseq=True) if query_params else ''
            # Rebuild URL
            url = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment
            ))

        return url

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string."""
        return json.loads(self.cors_origins)

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
