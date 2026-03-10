"""API routes for drinking session management."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas import (
    DrinkSession,
    DrinkSessionWithDrinks,
    ConsumedDrink,
    ConsumedDrinkCreate
)
from app.services import session_service


router = APIRouter()


@router.post("/session/start", response_model=DrinkSession)
async def start_session(
    db: AsyncSession = Depends(get_db)
):
    """
    Start a new drinking session (or get existing active session).

    Returns the active session.
    """
    session = await session_service.get_or_create_active_session(db=db)
    return session


@router.get("/session/current", response_model=DrinkSessionWithDrinks)
async def get_current_session(
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current active session with all consumed drinks.

    Returns session with consumed_drinks array populated.
    """
    session = await session_service.get_current_session_with_drinks(db=db)
    if not session:
        raise HTTPException(status_code=404, detail="No active session found")
    return session


@router.post("/session/consume", response_model=ConsumedDrink)
async def consume_drink(
    consumed_drink: ConsumedDrinkCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Add a drink to the current session.

    - **drink_id**: ID of the drink to consume
    - **notes**: Optional tasting notes
    """
    try:
        consumed = await session_service.consume_drink(
            db=db,
            drink_id=consumed_drink.drink_id,
            notes=consumed_drink.notes
        )
        return consumed
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/session/reset", response_model=DrinkSession)
async def reset_session(
    db: AsyncSession = Depends(get_db)
):
    """
    End the current session and start a fresh one.

    Returns the new active session.
    """
    new_session = await session_service.reset_session(db=db)
    return new_session


@router.get("/session/history", response_model=List[DrinkSessionWithDrinks])
async def get_session_history(
    db: AsyncSession = Depends(get_db)
):
    """
    Get past drinking sessions (most recent first).

    Returns up to 10 previous sessions with their consumed drinks.
    """
    sessions = await session_service.get_session_history(db=db, limit=10)
    return sessions
