from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.permission import Permission
from models.role import Role
from models.role_permissions import role_permissions
from schemas.role import PermissionCreate, RoleCreate
from services.exceptions import ConflictError, NotFoundError


async def create_role(db: AsyncSession, payload: RoleCreate) -> Role:
    role = Role(name=payload.name)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


async def get_role(db: AsyncSession, role_id: int) -> Role:
    role = await db.get(Role, role_id)
    if role is None:
        raise NotFoundError("Role not found")
    return role


async def create_permission(
    db: AsyncSession,
    payload: PermissionCreate,
) -> Permission:
    permission = Permission(name=payload.name)
    db.add(permission)
    await db.commit()
    await db.refresh(permission)
    return permission


async def assign_permission_to_role(
    db: AsyncSession,
    role_id: int,
    permission_id: int,
) -> None:
    role = await db.get(Role, role_id)
    if role is None:
        raise NotFoundError("Role not found")

    permission = await db.get(Permission, permission_id)
    if permission is None:
        raise NotFoundError("Permission not found")

    existing = await db.execute(
        select(role_permissions).where(
            role_permissions.c.role_id == role_id,
            role_permissions.c.permission_id == permission_id,
        )
    )
    if existing.first() is not None:
        raise ConflictError("Role already has permission")

    await db.execute(
        role_permissions.insert().values(
            role_id=role_id,
            permission_id=permission_id,
        )
    )
    await db.commit()
