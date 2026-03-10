from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal


# Drink Schemas
class FlavorProfile(BaseModel):
    """Flavor profile on 1-5 scale."""
    sweet: int
    bitter: int
    sour: int
    savory: int
    fruity: int


class DrinkBase(BaseModel):
    """Base drink schema."""
    name: str
    category: str
    subcategory: Optional[str] = None
    alcohol_content: Decimal
    flavor_profile: Dict[str, int]
    description: Optional[str] = None
    base_spirit: Optional[str] = None
    ingredients: Optional[List[str]] = None
    image_url: Optional[str] = None


class DrinkCreate(DrinkBase):
    """Schema for creating a drink."""
    pass


class Drink(DrinkBase):
    """Schema for drink response."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Session Schemas
class DrinkSessionBase(BaseModel):
    """Base session schema."""
    session_name: Optional[str] = None


class DrinkSessionCreate(DrinkSessionBase):
    """Schema for creating a session."""
    pass


class DrinkSession(DrinkSessionBase):
    """Schema for session response."""
    id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# Consumed Drink Schemas
class ConsumedDrinkBase(BaseModel):
    """Base consumed drink schema."""
    drink_id: int
    notes: Optional[str] = None


class ConsumedDrinkCreate(ConsumedDrinkBase):
    """Schema for consuming a drink."""
    pass


class ConsumedDrink(ConsumedDrinkBase):
    """Schema for consumed drink response."""
    id: int
    session_id: int
    consumed_at: datetime
    drink_order: int
    drink: Drink  # Include drink details

    model_config = ConfigDict(from_attributes=True)


# Session with consumed drinks
class DrinkSessionWithDrinks(DrinkSession):
    """Session with list of consumed drinks."""
    consumed_drinks: List[ConsumedDrink] = []

    model_config = ConfigDict(from_attributes=True)


# Recommendation Schemas
class RecommendationRequest(BaseModel):
    """Request for drink recommendations."""
    pass  # Can add optional filters later


class RecommendationResponse(BaseModel):
    """Response with AI-generated recommendations."""
    recommendations: List[str]
    reasoning: str
