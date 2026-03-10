"""API routes for drink pairing recommendations."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.pairing_service import pairing_service


router = APIRouter()


class PairingRequest(BaseModel):
    """Request model for pairing recommendations."""
    consumed_drinks: List[str]


class DrinkRecommendation(BaseModel):
    """Single drink recommendation with explanation."""
    drink_name: str
    explanation: str


class PairingResponse(BaseModel):
    """Response model for pairing recommendations."""
    good_combinations: List[DrinkRecommendation]
    okay_combinations: List[DrinkRecommendation]
    not_recommended: List[DrinkRecommendation]
    error: str | None = None


@router.post("/pairing/recommend", response_model=PairingResponse)
async def get_pairing_recommendations(
    request: PairingRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get drink pairing recommendations based on consumed drinks.

    - **consumed_drinks**: List of drink names the user has consumed

    Returns categorized recommendations:
    - **good_combinations**: Excellent pairings
    - **okay_combinations**: Acceptable pairings
    - **not_recommended**: Combinations to avoid
    """
    if not request.consumed_drinks:
        raise HTTPException(status_code=400, detail="Please provide at least one consumed drink")

    try:
        recommendations = await pairing_service.get_pairing_recommendations(
            consumed_drinks=request.consumed_drinks,
            db=db
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")
