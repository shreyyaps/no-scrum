from sqlalchemy.ext.asyncio import AsyncSession

from repositories import health_repo


async def check_database(db: AsyncSession) -> None:
    await health_repo.check_database(db)
