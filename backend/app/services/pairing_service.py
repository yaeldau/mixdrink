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
        try:
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
            # Fallback if parsing fails
            return {
                "good_combinations": [],
                "okay_combinations": [],
                "not_recommended": [],
                "error": f"Failed to parse recommendations: {str(e)}"
            }

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


# Singleton instance
pairing_service = PairingService()
