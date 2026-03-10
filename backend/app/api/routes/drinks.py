"""API routes for drink catalog."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas import Drink
from app.services import drink_service


router = APIRouter()


@router.get("/drinks", response_model=List[Drink])
async def get_drinks(
    search: Optional[str] = Query(None, description="Search term for drink name or description"),
    category: Optional[str] = Query(None, description="Filter by category (spirit, cocktail, wine, beer, liqueur)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=200, description="Max number of records to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of drinks with optional search and filters.

    - **search**: Search in name, description, subcategory
    - **category**: Filter by drink category
    - **skip**: Pagination offset
    - **limit**: Max results (1-200)
    """
    drinks = await drink_service.get_drinks(
        db=db,
        search=search,
        category=category,
        skip=skip,
        limit=limit
    )
    return drinks


@router.get("/drinks/{drink_id}", response_model=Drink)
async def get_drink(
    drink_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific drink by ID.

    - **drink_id**: Unique drink identifier
    """
    drink = await drink_service.get_drink_by_id(db=db, drink_id=drink_id)
    if not drink:
        raise HTTPException(status_code=404, detail=f"Drink with id {drink_id} not found")
    return drink


@router.get("/drinks/categories", response_model=List[str])
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    """Get list of unique drink categories."""
    categories = await drink_service.get_drink_categories(db=db)
    return categories
