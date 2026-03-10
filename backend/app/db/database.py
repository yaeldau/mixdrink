from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from app.config import settings

# Create async engine with pgbouncer workarounds
engine = create_async_engine(
    settings.db_url,
    echo=True,  # Log SQL queries (disable in production)
    future=True,
    poolclass=NullPool,  # Disable connection pooling (pgbouncer handles pooling)
    connect_args={
        "statement_cache_size": 0,  # Disable prepared statements for pgbouncer
        "server_settings": {
            "jit": "off"  # Disable JIT
        }
    },
    execution_options={
        "compiled_cache": None  # Disable SQL compilation caching
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
