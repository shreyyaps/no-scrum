from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from repositories import organization_repo, rbac_repo, role_repo, user_repo
from schemas.user import UserCreate
from services.exceptions import ConflictError, NotFoundError


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    organization = await organization_repo.get_by_id(db, payload.organization_id)
    if organization is None:
        raise NotFoundError("Organization not found")

    user = await user_repo.create(
        db,
        email=str(payload.email),
        name=payload.name,
        age=payload.age,
    )
    await organization_repo.create_membership(
        db=db,
        user_id=user.id,
        organization_id=payload.organization_id,
    )
    await db.commit()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, user_id: int) -> User:
    user = await user_repo.get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("User not found")
    return user


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    user = await user_repo.get_by_email(db, email)
    if user is None:
        raise NotFoundError("User not found")
    return user


async def assign_role_to_user(
    db: AsyncSession,
    user_id: int,
    role_id: int,
) -> None:
    user = await user_repo.get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("User not found")

    role = await role_repo.get_role_by_id(db, role_id)
    if role is None:
        raise NotFoundError("Role not found")

    if await user_repo.role_link_exists(db, user_id, role_id):
        raise ConflictError("User already has role")

    await user_repo.add_role(db, user_id, role_id)
    await db.commit()


async def get_user_permission_names(db: AsyncSession, user_id: int) -> list[str]:
    await get_user(db, user_id)
    return await rbac_repo.get_user_permission_names(db, user_id)
