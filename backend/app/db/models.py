from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Drink(Base):
    """Drink catalog - all available drinks."""
    __tablename__ = "drinks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)  # spirit, cocktail, wine, beer, liqueur
    subcategory = Column(String(100), nullable=True)  # vodka, whiskey, IPA, red_wine, etc.
    alcohol_content = Column(DECIMAL(4, 2), nullable=False)  # ABV percentage
    flavor_profile = Column(JSON, nullable=False)  # {sweet: 1-5, bitter: 1-5, sour: 1-5, savory: 1-5, fruity: 1-5}
    description = Column(Text, nullable=True)
    base_spirit = Column(String(100), nullable=True)  # For cocktails
    ingredients = Column(JSON, nullable=True)  # Array of strings
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    consumed_drinks = relationship("ConsumedDrink", back_populates="drink")


class DrinkSession(Base):
    """User's drinking session."""
    __tablename__ = "drink_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String(200), nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    # Relationships
    consumed_drinks = relationship("ConsumedDrink", back_populates="session", order_by="ConsumedDrink.drink_order")


class ConsumedDrink(Base):
    """Drinks consumed in a session."""
    __tablename__ = "consumed_drinks"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("drink_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    drink_id = Column(Integer, ForeignKey("drinks.id"), nullable=False, index=True)
    consumed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    drink_order = Column(Integer, nullable=False)  # 1st, 2nd, 3rd drink in session
    notes = Column(Text, nullable=True)

    # Relationships
    session = relationship("DrinkSession", back_populates="consumed_drinks")
    drink = relationship("Drink", back_populates="consumed_drinks")
