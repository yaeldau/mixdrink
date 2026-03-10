"""Service for generating drink pairing recommendations using Claude AI."""
from typing import List, Dict
from anthropic import Anthropic
from app.config import settings
from app.db.models import Drink
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json


class PairingService:
    """Service for AI-powered drink pairing recommendations."""

    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)

    async def get_pairing_recommendations(
        self,
        consumed_drinks: List[str],
        db: AsyncSession
    ) -> Dict:
        """
        Get drink pairing recommendations based on what the user has already consumed.

        Args:
            consumed_drinks: List of drink names the user has consumed
            db: Database session

        Returns:
            Dictionary with categorized recommendations
        """
        # Get all available drinks from database
        result = await db.execute(select(Drink))
        all_drinks = result.scalars().all()
        drink_names = [drink.name for drink in all_drinks]

        # Try AI recommendations first
        try:
            # Create prompt for Claude
            prompt = self._create_pairing_prompt(consumed_drinks, drink_names)

            # Call Claude API
            message = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=settings.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Parse response
            response_text = message.content[0].text

            # Extract JSON from response
            # Claude might wrap JSON in markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            recommendations = json.loads(response_text)
            return recommendations
        except Exception as e:
            # Fallback to rule-based recommendations if API fails
            return self._get_fallback_recommendations(consumed_drinks, all_drinks)

    def _create_pairing_prompt(self, consumed_drinks: List[str], available_drinks: List[str]) -> str:
        """Create the prompt for Claude API."""
        consumed_list = ", ".join(consumed_drinks)

        prompt = f"""You are an expert sommelier and mixologist. The user has consumed the following drinks: {consumed_list}

Based on what they've already had, recommend other alcoholic drinks that would pair well next. Consider flavor profiles, alcohol content progression, and classic pairing principles.

Available drinks to choose from:
{", ".join(available_drinks)}

Provide recommendations in THREE categories:

1. **Good Combinations** (3 drinks): Excellent pairings that complement what they've had
2. **Okay Combinations** (3 drinks): Acceptable pairings that won't clash but aren't ideal
3. **Not Recommended** (3 drinks): Combinations to avoid due to flavor clashes or overconsumption concerns

For each recommendation, provide:
- drink_name: The drink name (must match exactly from available drinks list)
- explanation: A brief 1-2 sentence explanation why

Return your response as a JSON object with this exact structure:
{{
  "good_combinations": [
    {{"drink_name": "...", "explanation": "..."}},
    {{"drink_name": "...", "explanation": "..."}},
    {{"drink_name": "...", "explanation": "..."}}
  ],
  "okay_combinations": [
    {{"drink_name": "...", "explanation": "..."}},
    {{"drink_name": "...", "explanation": "..."}},
    {{"drink_name": "...", "explanation": "..."}}
  ],
  "not_recommended": [
    {{"drink_name": "...", "explanation": "..."}},
    {{"drink_name": "...", "explanation": "..."}},
    {{"drink_name": "...", "explanation": "..."}}
  ]
}}

IMPORTANT: Return ONLY the JSON object, no additional text."""

        return prompt

    def _get_fallback_recommendations(self, consumed_drinks: List[str], all_drinks: List[Drink]) -> Dict:
        """
        Fallback rule-based recommendations when AI is unavailable.
        Provides simple category-based pairing logic.
        """
        import random

        # Categorize consumed drinks
        consumed_categories = set()
        for drink in all_drinks:
            if drink.name in consumed_drinks:
                consumed_categories.add(drink.category)

        # Get drinks not yet consumed
        available_drinks = [d for d in all_drinks if d.name not in consumed_drinks]

        # Simple pairing rules
        good = []
        okay = []
        not_recommended = []

        # Spirits pairing logic
        if "spirit" in consumed_categories or "cocktail" in consumed_categories:
            # Good: wines, lighter cocktails
            good = [d for d in available_drinks if d.category in ["wine", "liqueur"]][:3]
            # Okay: other spirits
            okay = [d for d in available_drinks if d.category == "spirit"][:3]
            # Not recommended: heavy beers
            not_recommended = [d for d in available_drinks if d.category == "beer"][:3]
        elif "wine" in consumed_categories:
            # Good: liqueurs, light cocktails
            good = [d for d in available_drinks if d.category in ["liqueur", "cocktail"]][:3]
            # Okay: other wines
            okay = [d for d in available_drinks if d.category == "wine"][:3]
            # Not recommended: strong spirits
            not_recommended = [d for d in available_drinks if d.category == "spirit"][:3]
        else:
            # Default: random selection
            random.shuffle(available_drinks)
            good = available_drinks[:3]
            okay = available_drinks[3:6]
            not_recommended = available_drinks[6:9]

        # Pad with random if not enough
        if len(good) < 3:
            remaining = [d for d in available_drinks if d not in good]
            random.shuffle(remaining)
            good.extend(remaining[:3 - len(good)])
        if len(okay) < 3:
            remaining = [d for d in available_drinks if d not in good and d not in okay]
            random.shuffle(remaining)
            okay.extend(remaining[:3 - len(okay)])
        if len(not_recommended) < 3:
            remaining = [d for d in available_drinks if d not in good and d not in okay and d not in not_recommended]
            random.shuffle(remaining)
            not_recommended.extend(remaining[:3 - len(not_recommended)])

        return {
            "good_combinations": [
                {
                    "drink_name": d.name,
                    "explanation": f"Pairs nicely with {consumed_drinks[0]} - complementary flavor profile."
                }
                for d in good[:3]
            ],
            "okay_combinations": [
                {
                    "drink_name": d.name,
                    "explanation": f"An acceptable choice after {consumed_drinks[0]} - won't clash significantly."
                }
                for d in okay[:3]
            ],
            "not_recommended": [
                {
                    "drink_name": d.name,
                    "explanation": f"May not pair well with {consumed_drinks[0]} - consider other options."
                }
                for d in not_recommended[:3]
            ]
        }


# Singleton instance
pairing_service = PairingService()
