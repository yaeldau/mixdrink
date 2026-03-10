"""Service layer for AI-powered drink recommendations using Claude."""
from typing import List, Dict, Any
from anthropic import Anthropic
from app.config import settings
from app.db.models import DrinkSession, ConsumedDrink, Drink


def build_recommendation_prompt(
    session: DrinkSession,
    consumed_drinks: List[ConsumedDrink],
    all_available_drinks: List[Drink]
) -> str:
    """
    Build the user prompt for Claude recommendation request.

    Args:
        session: Current drink session
        consumed_drinks: List of consumed drinks in order
        all_available_drinks: Full catalog of available drinks

    Returns:
        Formatted prompt string
    """
    # Calculate session stats
    total_drinks = len(consumed_drinks)
    total_alcohol = sum(
        float(cd.drink.alcohol_content) for cd in consumed_drinks
    )
    avg_alcohol = total_alcohol / total_drinks if total_drinks > 0 else 0

    # Build consumed drinks history
    history_lines = []
    for cd in consumed_drinks:
        drink = cd.drink
        fp = drink.flavor_profile
        history_lines.append(
            f"  {cd.drink_order}. {drink.name} ({drink.category}, "
            f"{float(drink.alcohol_content):.1f}% ABV)\n"
            f"     Flavors: Sweet:{fp.get('sweet', 0)}, Bitter:{fp.get('bitter', 0)}, "
            f"Sour:{fp.get('sour', 0)}, Savory:{fp.get('savory', 0)}, Fruity:{fp.get('fruity', 0)}\n"
            f"     Base: {drink.base_spirit or 'N/A'}"
        )

    history_text = "\n".join(history_lines) if history_lines else "  None yet"

    # Build available drinks catalog (sample for context)
    catalog_lines = []
    for drink in all_available_drinks[:50]:  # Limit to first 50 for prompt size
        catalog_lines.append(
            f"- {drink.name} ({drink.category}, {float(drink.alcohol_content):.1f}% ABV)"
        )
    catalog_text = "\n".join(catalog_lines)

    prompt = f"""Current Drinking Session Analysis:

Session Stats:
- Total drinks consumed: {total_drinks}
- Average ABV: {avg_alcohol:.1f}%
- Session duration: {_format_session_duration(session)}

Drinks Consumed (in order):
{history_text}

Available Drinks (sample of catalog):
{catalog_text}

Task: Based on the drinking progression above, recommend 3-5 specific drinks from the available catalog that would pair well as the next drink. Consider:

1. **Flavor Progression**: Build on or contrast with previous flavors
2. **Alcohol Pacing**: Don't spike ABV too quickly, consider alternating high/low
3. **Palate Cleansing**: Avoid same base spirit 3+ times in a row
4. **Session Context**: Early session = lighter drinks, later = digestifs or nightcaps

Format your response as:
**Recommendations:**
1. [Drink Name] - [Brief reasoning why it's a good next choice]
2. [Drink Name] - [Brief reasoning]
3. [Drink Name] - [Brief reasoning]

Be specific and reference the flavor/alcohol progression from their session."""

    return prompt


def _format_session_duration(session: DrinkSession) -> str:
    """Format session duration as human-readable string."""
    from datetime import datetime
    elapsed = datetime.utcnow() - session.started_at.replace(tzinfo=None)
    minutes = int(elapsed.total_seconds() / 60)
    if minutes < 60:
        return f"{minutes} minutes"
    hours = minutes // 60
    remaining_mins = minutes % 60
    return f"{hours}h {remaining_mins}m"


async def get_recommendations(
    session: DrinkSession,
    consumed_drinks: List[ConsumedDrink],
    all_drinks: List[Drink]
) -> Dict[str, Any]:
    """
    Get AI-powered drink recommendations using Claude.

    Args:
        session: Current drink session
        consumed_drinks: List of consumed drinks
        all_drinks: Full catalog of available drinks

    Returns:
        Dict with 'recommendations' (list of str) and 'reasoning' (str)
    """
    # Initialize Anthropic client
    client = Anthropic(api_key=settings.anthropic_api_key)

    # Build prompt
    user_prompt = build_recommendation_prompt(session, consumed_drinks, all_drinks)

    # System prompt for mixologist role
    system_prompt = """You are an expert mixologist and sommelier with deep knowledge of:
- Flavor pairing and cocktail theory
- Alcohol progression and pacing
- Palate cleansing and taste fatigue
- Classic and modern drink combinations

Your goal is to suggest drinks that enhance the user's drinking experience based on
what they've already consumed. Consider the full flavor journey, not just individual drinks.

Always recommend specific drinks by name from the available catalog. Be concise but insightful."""

    # Call Claude API
    try:
        message = client.messages.create(
            model=settings.claude_model,
            max_tokens=settings.max_tokens,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        # Extract response
        response_text = message.content[0].text

        # Parse recommendations (simple parsing - extract drink names from numbered list)
        recommendations = _parse_recommendations(response_text)

        return {
            "recommendations": recommendations,
            "reasoning": response_text
        }

    except Exception as e:
        # Fallback recommendations if API fails
        return {
            "recommendations": [
                "Martini - Classic and refreshing",
                "Old Fashioned - Timeless whiskey cocktail",
                "Mojito - Light and minty"
            ],
            "reasoning": f"API error: {str(e)}. Showing fallback recommendations."
        }


def _parse_recommendations(response_text: str) -> List[str]:
    """
    Parse drink recommendations from Claude's response.

    Extracts drink names from numbered list format.

    Args:
        response_text: Full Claude API response

    Returns:
        List of recommendation strings with drink name and reasoning
    """
    recommendations = []
    lines = response_text.split('\n')

    for line in lines:
        line = line.strip()
        # Match numbered list items: "1. Drink Name - reasoning" or "1. Drink Name: reasoning"
        if line and (line[0].isdigit() or line.startswith('-')):
            # Remove leading number/bullet
            cleaned = line.lstrip('0123456789.-) ')
            if cleaned:
                recommendations.append(cleaned)

    # Return first 5 recommendations
    return recommendations[:5] if recommendations else [response_text]


async def get_simple_recommendations(
    consumed_drinks: List[ConsumedDrink],
    all_drinks: List[Drink]
) -> List[str]:
    """
    Get simple rule-based recommendations without AI (fallback).

    Args:
        consumed_drinks: List of consumed drinks
        all_drinks: Full catalog of available drinks

    Returns:
        List of recommended drink names
    """
    if not consumed_drinks:
        # No drinks yet - suggest popular starters
        return [
            "Aperol Spritz - Light and refreshing aperitif",
            "Gin & Tonic - Classic and clean",
            "Mojito - Minty and refreshing"
        ]

    last_drink = consumed_drinks[-1].drink
    last_category = last_drink.category
    last_abv = float(last_drink.alcohol_content)

    recommendations = []

    # Rule 1: If last was high ABV, suggest lower ABV
    if last_abv > 30:
        for drink in all_drinks:
            if float(drink.alcohol_content) < 15 and drink.category in ["beer", "wine"]:
                recommendations.append(f"{drink.name} - Lower ABV to slow down")
                if len(recommendations) >= 2:
                    break

    # Rule 2: Vary the category
    for drink in all_drinks:
        if drink.category != last_category and len(recommendations) < 5:
            recommendations.append(f"{drink.name} - Different category for variety")

    return recommendations[:5]
