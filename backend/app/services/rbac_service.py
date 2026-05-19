from sqlalchemy.ext.asyncio import AsyncSession

from repositories import rbac_repo


async def get_user_permission_names(db: AsyncSession, user_id: int) -> list[str]:
    return await rbac_repo.get_user_permission_names(db, user_id)


async def user_has_permission(
    db: AsyncSession,
    user_id: int,
    permission_name: str,
) -> bool:
    permissions = await get_user_permission_names(db, user_id)
    return permission_name in permissions


async def identity_has_permission(
    db: AsyncSession,
    email: str,
    permission_name: str,
) -> bool:
    user_id = await rbac_repo.get_user_id_by_email(db, email)
    if user_id is None:
        return False
    return await user_has_permission(db, user_id, permission_name)
