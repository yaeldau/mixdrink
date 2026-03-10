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
        Provides category-based pairing logic with general drink types.
        """
        import random

        # Map consumed drinks to their details
        consumed_details = []
        for drink in all_drinks:
            if drink.name in consumed_drinks:
                consumed_details.append({
                    'name': drink.name,
                    'category': drink.category,
                    'subcategory': drink.subcategory
                })

        # Group drinks by subcategory (for general recommendations)
        subcategory_groups = {}
        for drink in all_drinks:
            if drink.subcategory not in subcategory_groups:
                subcategory_groups[drink.subcategory] = []
            subcategory_groups[drink.subcategory].append(drink)

        # Get unique subcategories not consumed
        consumed_subcategories = {d['subcategory'] for d in consumed_details}
        available_subcategories = [
            sub for sub in subcategory_groups.keys()
            if sub not in consumed_subcategories
        ]

        # Define pairing rules
        def get_category_name(subcategory: str) -> str:
            """Convert subcategory to readable name."""
            names = {
                'vodka': 'Vodka',
                'gin': 'Gin',
                'rum': 'Rum',
                'tequila': 'Tequila',
                'whiskey': 'Whiskey',
                'bourbon': 'Bourbon',
                'scotch': 'Scotch',
                'rye': 'Rye Whiskey',
                'irish_whiskey': 'Irish Whiskey',
                'cognac': 'Cognac',
                'brandy': 'Brandy',
                'mezcal': 'Mezcal',
                'pisco': 'Pisco',
                'sake': 'Sake',
                'red_wine': 'Red Wine',
                'white_wine': 'White Wine',
                'sparkling': 'Sparkling Wine',
                'beer': 'Beer',
                'ipa': 'IPA Beer',
                'stout': 'Stout Beer',
                'lager': 'Lager Beer',
                'liqueur': 'Liqueur',
                'cocktail': 'Cocktails'
            }
            return names.get(subcategory, subcategory.replace('_', ' ').title())

        def get_explanation(subcategory: str, rating: str, consumed: list) -> str:
            """Generate explanation based on consumed drinks and rating."""
            consumed_types = [get_category_name(d['subcategory']) for d in consumed]
            consumed_str = ' and '.join(consumed_types) if len(consumed_types) <= 2 else ', '.join(consumed_types[:-1]) + f', and {consumed_types[-1]}'

            drink_type = get_category_name(subcategory)

            if rating == 'good':
                reasons = [
                    f"{drink_type} complements the flavors you've been enjoying.",
                    f"After {consumed_str}, {drink_type} offers a nice flavor progression.",
                    f"{drink_type} pairs well with the drink profile you've established.",
                ]
            elif rating == 'okay':
                reasons = [
                    f"{drink_type} won't clash, but may not be the most interesting choice.",
                    f"A safe option after {consumed_str}, though not the most exciting pairing.",
                    f"{drink_type} is acceptable, but consider our top recommendations first.",
                ]
            else:  # not recommended
                reasons = [
                    f"{drink_type} may clash with {consumed_str} - can cause flavor fatigue.",
                    f"After {consumed_str}, {drink_type} could be overwhelming or unbalanced.",
                    f"Mixing {consumed_str} with {drink_type} isn't ideal - try our better pairings instead.",
                ]

            return random.choice(reasons)

        # Simple pairing logic based on what's consumed
        good_subs = []
        okay_subs = []
        bad_subs = []

        # Check what categories were consumed
        has_spirit = any(d['category'] == 'spirit' for d in consumed_details)
        has_wine = any(d['category'] == 'wine' for d in consumed_details)
        has_beer = any(d['category'] == 'beer' for d in consumed_details)
        has_cocktail = any(d['category'] == 'cocktail' for d in consumed_details)

        if has_spirit or has_cocktail:
            # After spirits/cocktails: wines good, liqueurs okay, more spirits risky
            good_subs = [s for s in available_subcategories if s in ['red_wine', 'white_wine', 'sparkling', 'liqueur']]
            okay_subs = [s for s in available_subcategories if s in ['cocktail', 'beer', 'lager']]
            bad_subs = [s for s in available_subcategories if s in ['vodka', 'gin', 'rum', 'tequila', 'whiskey', 'stout']]
        elif has_wine:
            # After wine: liqueurs good, light drinks okay, strong spirits not recommended
            good_subs = [s for s in available_subcategories if s in ['liqueur', 'sparkling', 'cocktail']]
            okay_subs = [s for s in available_subcategories if s in ['red_wine', 'white_wine', 'beer']]
            bad_subs = [s for s in available_subcategories if s in ['vodka', 'gin', 'rum', 'tequila', 'whiskey', 'ipa', 'stout']]
        elif has_beer:
            # After beer: similar beers okay, wines good, strong spirits not great
            good_subs = [s for s in available_subcategories if s in ['white_wine', 'sparkling', 'lager']]
            okay_subs = [s for s in available_subcategories if s in ['beer', 'ipa', 'cocktail']]
            bad_subs = [s for s in available_subcategories if s in ['vodka', 'whiskey', 'red_wine', 'stout']]
        else:
            # Default: random distribution
            random.shuffle(available_subcategories)
            good_subs = available_subcategories[:3]
            okay_subs = available_subcategories[3:6]
            bad_subs = available_subcategories[6:9]

        # Pad lists if needed
        all_available = set(available_subcategories)
        used = set()

        while len(good_subs) < 3 and len(all_available - used) > 0:
            remaining = list(all_available - used - set(okay_subs) - set(bad_subs))
            if remaining:
                good_subs.append(remaining[0])
                used.add(remaining[0])

        while len(okay_subs) < 3 and len(all_available - used) > 0:
            remaining = list(all_available - used - set(good_subs) - set(bad_subs))
            if remaining:
                okay_subs.append(remaining[0])
                used.add(remaining[0])

        while len(bad_subs) < 3 and len(all_available - used) > 0:
            remaining = list(all_available - used - set(good_subs) - set(okay_subs))
            if remaining:
                bad_subs.append(remaining[0])
                used.add(remaining[0])

        return {
            "good_combinations": [
                {
                    "drink_name": get_category_name(sub),
                    "explanation": get_explanation(sub, 'good', consumed_details)
                }
                for sub in good_subs[:3]
            ],
            "okay_combinations": [
                {
                    "drink_name": get_category_name(sub),
                    "explanation": get_explanation(sub, 'okay', consumed_details)
                }
                for sub in okay_subs[:3]
            ],
            "not_recommended": [
                {
                    "drink_name": get_category_name(sub),
                    "explanation": get_explanation(sub, 'bad', consumed_details)
                }
                for sub in bad_subs[:3]
            ]
        }


# Singleton instance
pairing_service = PairingService()
