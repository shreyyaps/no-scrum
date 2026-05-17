from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.auth import AuthIdentity, get_current_identity
from dependencies.db import get_db
from services import rbac_service


def require_permission(permission_name: str) -> Callable[..., object]:
    async def permission_dependency(
        identity: AuthIdentity = Depends(get_current_identity),
        db: AsyncSession = Depends(get_db),
    ) -> AuthIdentity:
        has_permission = await rbac_service.identity_has_permission(
            db=db,
            email=identity.email,
            permission_name=permission_name,
        )
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )
        return identity

    return permission_dependency
