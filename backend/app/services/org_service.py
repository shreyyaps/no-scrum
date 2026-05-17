from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from models.organization_user import OrganizationUser
from models.user import User
from schemas.organization import OrganizationCreate
from services.exceptions import ConflictError, NotFoundError


async def create_organization(
    db: AsyncSession,
    payload: OrganizationCreate,
) -> Organization:
    organization = Organization(name=payload.name)
    db.add(organization)
    await db.commit()
    await db.refresh(organization)
    return organization


async def get_organization(db: AsyncSession, organization_id: int) -> Organization:
    organization = await db.get(Organization, organization_id)
    if organization is None:
        raise NotFoundError("Organization not found")
    return organization


async def assign_user_to_organization(
    db: AsyncSession,
    user_id: int,
    organization_id: int,
) -> OrganizationUser:
    user = await db.get(User, user_id)
    if user is None:
        raise NotFoundError("User not found")

    organization = await db.get(Organization, organization_id)
    if organization is None:
        raise NotFoundError("Organization not found")

    existing = await db.get(OrganizationUser, user_id)
    if existing is not None:
        if existing.organization_id == organization_id:
            return existing
        raise ConflictError("User already belongs to an organization")

    membership = OrganizationUser(user_id=user_id, organization_id=organization_id)
    db.add(membership)
    await db.commit()
    await db.refresh(membership)
    return membership


async def list_organization_users(
    db: AsyncSession,
    organization_id: int,
) -> list[OrganizationUser]:
    await get_organization(db, organization_id)
    result = await db.execute(
        select(OrganizationUser).where(
            OrganizationUser.organization_id == organization_id,
        )
    )
    return list(result.scalars().all())
