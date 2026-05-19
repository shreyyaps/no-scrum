from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from models.organization_user import OrganizationUser
from repositories import organization_repo, user_repo
from schemas.organization import OrganizationCreate
from services.exceptions import ConflictError, NotFoundError


async def create_organization(
    db: AsyncSession,
    payload: OrganizationCreate,
) -> Organization:
    organization = await organization_repo.create(db, payload.name)
    await db.commit()
    await db.refresh(organization)
    return organization


async def get_organization(db: AsyncSession, organization_id: int) -> Organization:
    organization = await organization_repo.get_by_id(db, organization_id)
    if organization is None:
        raise NotFoundError("Organization not found")
    return organization


async def assign_user_to_organization(
    db: AsyncSession,
    user_id: int,
    organization_id: int,
) -> OrganizationUser:
    user = await user_repo.get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("User not found")

    organization = await organization_repo.get_by_id(db, organization_id)
    if organization is None:
        raise NotFoundError("Organization not found")

    existing = await organization_repo.get_membership_by_user_id(db, user_id)
    if existing is not None:
        if existing.organization_id == organization_id:
            return existing
        raise ConflictError("User already belongs to an organization")

    membership = await organization_repo.create_membership(
        db=db,
        user_id=user_id,
        organization_id=organization_id,
    )
    await db.commit()
    await db.refresh(membership)
    return membership


async def list_organization_users(
    db: AsyncSession,
    organization_id: int,
) -> list[OrganizationUser]:
    await get_organization(db, organization_id)
    return await organization_repo.list_users(db, organization_id)
