from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from models.organization_user import OrganizationUser


async def create(
    db: AsyncSession,
    name: str,
    description: str | None = None,
) -> Organization:
    organization = Organization(name=name, description=description)
    db.add(organization)
    await db.flush()
    return organization


async def get_by_id(
    db: AsyncSession,
    organization_id: int,
) -> Organization | None:
    return await db.get(Organization, organization_id)


async def get_membership_by_user_id(
    db: AsyncSession,
    user_id: int,
) -> OrganizationUser | None:
    return await db.get(OrganizationUser, user_id)


async def create_membership(
    db: AsyncSession,
    user_id: int,
    organization_id: int,
) -> OrganizationUser:
    membership = OrganizationUser(user_id=user_id, organization_id=organization_id)
    db.add(membership)
    await db.flush()
    return membership


async def list_users(
    db: AsyncSession,
    organization_id: int,
) -> list[OrganizationUser]:
    result = await db.execute(
        select(OrganizationUser).where(
            OrganizationUser.organization_id == organization_id,
        )
    )
    return list(result.scalars().all())
