from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from app.config import settings

# Create async engine
# CRITICAL WORKAROUND FOR VERCEL POSTGRES + PGBOUNCER:
# Even POSTGRES_URL_NON_POOLING uses pgbouncer, so we need to disable prepared statements
# by using NullPool and relying on the statement_cache_size parameter in the URL
engine = create_async_engine(
    settings.db_url,
    echo=True,  # Log SQL queries (disable in production)
    poolclass=NullPool,  # Disable SQLAlchemy pooling (let pgbouncer handle it)
    connect_args={
        "statement_cache_size": 0,  # Disable asyncpg prepared statements
        "server_settings": {
            "jit": "off",  # Disable JIT
            "application_name": "mixdrink"
        }
    },
    execution_options={
        "compiled_cache": None,  # Disable SQL compilation caching
        "schema_translate_map": None
    }
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
