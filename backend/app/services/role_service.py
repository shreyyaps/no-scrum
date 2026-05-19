from sqlalchemy.ext.asyncio import AsyncSession

from models.permission import Permission
from models.role import Role
from repositories import role_repo
from schemas.role import PermissionCreate, RoleCreate
from services.exceptions import ConflictError, NotFoundError


async def create_role(db: AsyncSession, payload: RoleCreate) -> Role:
    role = await role_repo.create_role(db, payload.name)
    await db.commit()
    await db.refresh(role)
    return role


async def get_role(db: AsyncSession, role_id: int) -> Role:
    role = await role_repo.get_role_by_id(db, role_id)
    if role is None:
        raise NotFoundError("Role not found")
    return role


async def create_permission(
    db: AsyncSession,
    payload: PermissionCreate,
) -> Permission:
    permission = await role_repo.create_permission(db, payload.name)
    await db.commit()
    await db.refresh(permission)
    return permission


async def assign_permission_to_role(
    db: AsyncSession,
    role_id: int,
    permission_id: int,
) -> None:
    role = await role_repo.get_role_by_id(db, role_id)
    if role is None:
        raise NotFoundError("Role not found")

    permission = await role_repo.get_permission_by_id(db, permission_id)
    if permission is None:
        raise NotFoundError("Permission not found")

    if await role_repo.permission_link_exists(db, role_id, permission_id):
        raise ConflictError("Role already has permission")

    await role_repo.add_permission(db, role_id, permission_id)
    await db.commit()
