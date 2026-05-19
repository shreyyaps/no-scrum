from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.permission import Permission
from models.role import Role
from models.role_permissions import role_permissions
from models.user import User
from models.user_roles import user_roles


async def get_user_permission_names(db: AsyncSession, user_id: int) -> list[str]:
    result = await db.execute(
        select(Permission.name)
        .join(
            role_permissions,
            role_permissions.c.permission_id == Permission.id,
        )
        .join(Role, Role.id == role_permissions.c.role_id)
        .join(user_roles, user_roles.c.role_id == Role.id)
        .where(user_roles.c.user_id == user_id)
        .distinct()
    )
    return list(result.scalars().all())


async def get_user_id_by_email(db: AsyncSession, email: str) -> int | None:
    result = await db.execute(select(User.id).where(User.email == email))
    return result.scalar_one_or_none()
