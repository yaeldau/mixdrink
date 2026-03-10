from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="MixDrink API",
    description="AI-powered drink pairing recommendations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "mixdrink-api"}


@app.get("/api/debug/db-url")
async def debug_db_url():
    """Debug endpoint to check which database URL is being used."""
    from app.config import settings
    from urllib.parse import urlparse

    parsed = urlparse(settings.db_url)
    # Mask password for security
    masked_url = f"{parsed.scheme}://{parsed.username}:****@{parsed.hostname}:{parsed.port}{parsed.path}"

    return {
        "using_non_pooling": settings.postgres_url_non_pooling is not None,
        "using_postgres_url": settings.postgres_url is not None,
        "masked_url": masked_url,
        "has_statement_cache_param": "statement_cache_size" in (parsed.query or "")
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "MixDrink API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/api/init-db")
async def init_database():
    """Initialize database tables and seed data."""
    from app.db.database import engine, Base, AsyncSessionLocal
    from app.db.models import Drink
    from app.db.seed_data import DRINKS_DATA
    from sqlalchemy import select

    try:
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Seed drinks if empty
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Drink))
            existing_drinks = result.scalars().all()

            if not existing_drinks:
                drinks_to_add = [Drink(**drink_data) for drink_data in DRINKS_DATA]
                session.add_all(drinks_to_add)
                await session.commit()
                return {"status": "success", "message": f"Database initialized and seeded with {len(drinks_to_add)} drinks"}
            else:
                return {"status": "success", "message": f"Database already contains {len(existing_drinks)} drinks"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


# Route registration
from app.api.routes import drinks, session, recommendations

app.include_router(drinks.router, prefix="/api", tags=["drinks"])
app.include_router(session.router, prefix="/api", tags=["session"])
app.include_router(recommendations.router, prefix="/api", tags=["recommendations"])
