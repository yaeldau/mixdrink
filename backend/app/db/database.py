from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings
from urllib.parse import urlparse
import asyncpg


async def create_asyncpg_connection():
    """
    Create asyncpg connection with statement_cache_size=0 for pgbouncer compatibility.
    This is a workaround for Vercel Postgres which uses pgbouncer in transaction mode.
    """
    # Get clean database URL
    db_url = settings.db_url

    # Parse URL to extract connection parameters
    # Convert postgresql+asyncpg:// back to postgres:// for parsing
    url_for_parsing = db_url.replace("postgresql+asyncpg://", "postgres://")
    parsed = urlparse(url_for_parsing)

    # Extract connection details
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port or 5432
    database = parsed.path.lstrip('/') if parsed.path else 'postgres'

    # Create connection with statement_cache_size=0 to disable prepared statements
    conn = await asyncpg.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        statement_cache_size=0,  # CRITICAL: Disables prepared statements for pgbouncer
        timeout=60
    )

    return conn


# Create async engine using custom connection function
engine = create_async_engine(
    settings.db_url,
    echo=True,  # Log SQL queries (disable in production)
    future=True,
    async_creator=create_asyncpg_connection,  # Use custom connection function
    pool_pre_ping=True  # Verify connections before using
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for ORM models
Base = declarative_base()


async def get_db():
    """Dependency for getting async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
