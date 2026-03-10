"""API routes for AI-powered drink recommendations."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas import RecommendationRequest, RecommendationResponse
from app.services import session_service, drink_service, recommendation_service


router = APIRouter()


@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get AI-powered drink recommendations based on current session.

    Uses Claude API to analyze the drinking session and suggest intelligent
    next drinks considering:
    - Flavor progression
    - Alcohol pacing
    - Palate cleansing
    - Session context

    Returns 3-5 recommended drinks with reasoning.
    """
    # Get current session with consumed drinks
    session = await session_service.get_current_session_with_drinks(db=db)
    if not session:
        raise HTTPException(
            status_code=404,
            detail="No active session found. Start a session and consume at least one drink."
        )

    # Get full drink catalog for recommendations
    all_drinks = await drink_service.get_drinks(db=db, limit=200)

    # Get AI recommendations
    result = await recommendation_service.get_recommendations(
        session=session,
        consumed_drinks=session.consumed_drinks,
        all_drinks=all_drinks
    )

    return RecommendationResponse(
        recommendations=result["recommendations"],
        reasoning=result["reasoning"]
    )
