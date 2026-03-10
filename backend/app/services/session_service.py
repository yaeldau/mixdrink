"""Service layer for drinking session management."""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from app.db.models import DrinkSession, ConsumedDrink, Drink


async def get_or_create_active_session(db: AsyncSession) -> DrinkSession:
    """
    Get the current active session, or create a new one if none exists.

    Args:
        db: Database session

    Returns:
        Active DrinkSession
    """
    # Check for existing active session
    result = await db.execute(
        select(DrinkSession)
        .where(DrinkSession.is_active == True)
        .order_by(DrinkSession.started_at.desc())
    )
    session = result.scalar_one_or_none()

    if session:
        return session

    # Create new session
    new_session = DrinkSession(
        session_name=f"Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        is_active=True
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session


async def get_session_with_drinks(db: AsyncSession, session_id: int) -> Optional[DrinkSession]:
    """
    Get a session with all consumed drinks eagerly loaded.

    Args:
        db: Database session
        session_id: Session ID

    Returns:
        DrinkSession with consumed_drinks populated, or None
    """
    result = await db.execute(
        select(DrinkSession)
        .options(
            selectinload(DrinkSession.consumed_drinks).selectinload(ConsumedDrink.drink)
        )
        .where(DrinkSession.id == session_id)
    )
    return result.scalar_one_or_none()


async def get_current_session_with_drinks(db: AsyncSession) -> Optional[DrinkSession]:
    """
    Get the active session with all consumed drinks.

    Args:
        db: Database session

    Returns:
        Active DrinkSession with drinks, or None
    """
    result = await db.execute(
        select(DrinkSession)
        .options(
            selectinload(DrinkSession.consumed_drinks).selectinload(ConsumedDrink.drink)
        )
        .where(DrinkSession.is_active == True)
        .order_by(DrinkSession.started_at.desc())
    )
    return result.scalar_one_or_none()


async def consume_drink(
    db: AsyncSession,
    drink_id: int,
    notes: Optional[str] = None
) -> ConsumedDrink:
    """
    Add a drink to the current active session.

    Args:
        db: Database session
        drink_id: ID of the drink to consume
        notes: Optional tasting notes

    Returns:
        ConsumedDrink object

    Raises:
        ValueError: If drink_id doesn't exist
    """
    # Get or create active session
    session = await get_or_create_active_session(db)

    # Verify drink exists
    drink_result = await db.execute(
        select(Drink).where(Drink.id == drink_id)
    )
    drink = drink_result.scalar_one_or_none()
    if not drink:
        raise ValueError(f"Drink with id {drink_id} not found")

    # Calculate drink order (1-indexed)
    count_result = await db.execute(
        select(ConsumedDrink)
        .where(ConsumedDrink.session_id == session.id)
    )
    existing_count = len(count_result.scalars().all())
    drink_order = existing_count + 1

    # Create consumed drink record
    consumed = ConsumedDrink(
        session_id=session.id,
        drink_id=drink_id,
        drink_order=drink_order,
        notes=notes
    )
    db.add(consumed)
    await db.commit()
    await db.refresh(consumed)

    # Eagerly load the drink relationship
    await db.refresh(consumed, ["drink"])

    return consumed


async def end_session(db: AsyncSession, session_id: int) -> DrinkSession:
    """
    Mark a session as ended.

    Args:
        db: Database session
        session_id: Session ID to end

    Returns:
        Updated DrinkSession

    Raises:
        ValueError: If session doesn't exist
    """
    result = await db.execute(
        select(DrinkSession).where(DrinkSession.id == session_id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise ValueError(f"Session with id {session_id} not found")

    session.is_active = False
    session.ended_at = datetime.utcnow()
    await db.commit()
    await db.refresh(session)
    return session


async def reset_session(db: AsyncSession) -> DrinkSession:
    """
    End the current active session and create a new one.

    Args:
        db: Database session

    Returns:
        New active DrinkSession
    """
    # End current active session if exists
    result = await db.execute(
        select(DrinkSession).where(DrinkSession.is_active == True)
    )
    current_session = result.scalar_one_or_none()

    if current_session:
        current_session.is_active = False
        current_session.ended_at = datetime.utcnow()

    # Create new session
    new_session = DrinkSession(
        session_name=f"Session {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        is_active=True
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session


async def get_session_history(db: AsyncSession, limit: int = 10) -> List[DrinkSession]:
    """
    Get past sessions ordered by most recent.

    Args:
        db: Database session
        limit: Max number of sessions to return

    Returns:
        List of DrinkSession objects
    """
    result = await db.execute(
        select(DrinkSession)
        .options(selectinload(DrinkSession.consumed_drinks).selectinload(ConsumedDrink.drink))
        .where(DrinkSession.is_active == False)
        .order_by(DrinkSession.started_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())
