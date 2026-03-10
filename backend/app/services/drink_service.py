"""Service layer for drink catalog operations."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.db.models import Drink


async def get_drinks(
    db: AsyncSession,
    search: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Drink]:
    """
    Get drinks with optional search and filter.

    Args:
        db: Database session
        search: Search term for name or description
        category: Filter by category (spirit, cocktail, wine, beer, liqueur)
        skip: Number of records to skip (pagination)
        limit: Max number of records to return

    Returns:
        List of Drink objects
    """
    query = select(Drink)

    # Apply search filter
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Drink.name.ilike(search_term),
                Drink.description.ilike(search_term),
                Drink.subcategory.ilike(search_term)
            )
        )

    # Apply category filter
    if category:
        query = query.where(Drink.category == category)

    # Apply pagination and ordering
    query = query.order_by(Drink.name).offset(skip).limit(limit)

    result = await db.execute(query)
    drinks = result.scalars().all()
    return list(drinks)


async def get_drink_by_id(db: AsyncSession, drink_id: int) -> Optional[Drink]:
    """
    Get a specific drink by ID.

    Args:
        db: Database session
        drink_id: Drink ID

    Returns:
        Drink object or None if not found
    """
    result = await db.execute(
        select(Drink).where(Drink.id == drink_id)
    )
    return result.scalar_one_or_none()


async def get_drinks_by_ids(db: AsyncSession, drink_ids: List[int]) -> List[Drink]:
    """
    Get multiple drinks by IDs.

    Args:
        db: Database session
        drink_ids: List of drink IDs

    Returns:
        List of Drink objects
    """
    result = await db.execute(
        select(Drink).where(Drink.id.in_(drink_ids))
    )
    return list(result.scalars().all())


async def get_drink_categories(db: AsyncSession) -> List[str]:
    """
    Get list of unique drink categories.

    Args:
        db: Database session

    Returns:
        List of category names
    """
    from sqlalchemy import distinct
    result = await db.execute(
        select(distinct(Drink.category)).order_by(Drink.category)
    )
    return list(result.scalars().all())
