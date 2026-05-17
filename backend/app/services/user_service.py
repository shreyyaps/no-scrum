from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.organization import Organization
from models.organization_user import OrganizationUser
from models.role import Role
from models.user import User
from models.user_roles import user_roles
from schemas.user import UserCreate
from services import rbac_service
from services.exceptions import ConflictError, NotFoundError


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    organization = await db.get(Organization, payload.organization_id)
    if organization is None:
        raise NotFoundError("Organization not found")

    user = User(email=str(payload.email))
    db.add(user)
    await db.flush()

    db.add(
        OrganizationUser(
            user_id=user.id,
            organization_id=payload.organization_id,
        )
    )
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int) -> User:
    user = await db.get(User, user_id)
    if user is None:
        raise NotFoundError("User not found")
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise NotFoundError("User not found")
    return user


async def assign_role_to_user(
    db: AsyncSession,
    user_id: int,
    role_id: int,
) -> None:
    user = await db.get(User, user_id)
    if user is None:
        raise NotFoundError("User not found")

    role = await db.get(Role, role_id)
    if role is None:
        raise NotFoundError("Role not found")

    existing = await db.execute(
        select(user_roles).where(
            user_roles.c.user_id == user_id,
            user_roles.c.role_id == role_id,
        )
    )
    if existing.first() is not None:
        raise ConflictError("User already has role")

    await db.execute(user_roles.insert().values(user_id=user_id, role_id=role_id))
    await db.commit()


async def get_user_permission_names(db: AsyncSession, user_id: int) -> list[str]:
    await get_user(db, user_id)
    return await rbac_service.get_user_permission_names(db, user_id)
