from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.db.database import engine, Base
from app.db.models import Drink
from app.db.seed_data import DRINKS_DATA
from sqlalchemy import select
from app.db.database import AsyncSessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup."""
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
            print(f"Seeded {len(drinks_to_add)} drinks")

    yield

    # Cleanup
    await engine.dispose()


app = FastAPI(
    title="MixDrink API",
    description="AI-powered drink pairing recommendations",
    version="1.0.0",
    lifespan=lifespan
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


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "MixDrink API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Route registration
from app.api.routes import drinks, session, recommendations

app.include_router(drinks.router, prefix="/api", tags=["drinks"])
app.include_router(session.router, prefix="/api", tags=["session"])
app.include_router(recommendations.router, prefix="/api", tags=["recommendations"])
