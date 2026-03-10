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
