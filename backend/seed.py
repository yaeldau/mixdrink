"""Seed database with drink data."""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal, engine
from app.db.models import Drink
from app.db.seed_data import DRINKS_DATA


async def seed_drinks():
    """Seed the drinks table with initial data."""
    async with AsyncSessionLocal() as session:
        # Check if drinks already exist
        from sqlalchemy import select
        result = await session.execute(select(Drink))
        existing_drinks = result.scalars().all()

        if existing_drinks:
            print(f"Database already contains {len(existing_drinks)} drinks. Skipping seed.")
            return

        # Add all drinks
        drinks_to_add = []
        for drink_data in DRINKS_DATA:
            drink = Drink(**drink_data)
            drinks_to_add.append(drink)

        session.add_all(drinks_to_add)
        await session.commit()
        print(f"Successfully seeded {len(drinks_to_add)} drinks to the database!")


async def main():
    """Main entry point for seeding."""
    print("Starting database seeding...")
    await seed_drinks()
    print("Seeding complete!")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
