from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.permission import Permission
from models.role import Role
from models.role_permissions import role_permissions


async def create_role(
    db: AsyncSession,
    name: str,
    description: str | None = None,
) -> Role:
    role = Role(name=name, description=description)
    db.add(role)
    await db.flush()
    return role


async def get_role_by_id(db: AsyncSession, role_id: int) -> Role | None:
    return await db.get(Role, role_id)


async def create_permission(
    db: AsyncSession,
    name: str,
    description: str | None = None,
) -> Permission:
    permission = Permission(name=name, description=description)
    db.add(permission)
    await db.flush()
    return permission


async def get_permission_by_id(
    db: AsyncSession,
    permission_id: int,
) -> Permission | None:
    return await db.get(Permission, permission_id)


async def permission_link_exists(
    db: AsyncSession,
    role_id: int,
    permission_id: int,
) -> bool:
    result = await db.execute(
        select(role_permissions).where(
            role_permissions.c.role_id == role_id,
            role_permissions.c.permission_id == permission_id,
        )
    )
    return result.first() is not None


async def add_permission(
    db: AsyncSession,
    role_id: int,
    permission_id: int,
) -> None:
    await db.execute(
        role_permissions.insert().values(
            role_id=role_id,
            permission_id=permission_id,
        )
    )
