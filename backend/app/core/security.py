from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from services import rbac_service


@dataclass(frozen=True)
class AuthIdentity:
    subject: str
    email: str


async def get_current_identity(
    x_auth_subject: Annotated[str | None, Header(alias="X-Auth-Subject")] = None,
    x_auth_email: Annotated[str | None, Header(alias="X-Auth-Email")] = None,
) -> AuthIdentity:
    """Identity supplied by a third-party auth provider or auth gateway."""
    if not x_auth_subject or not x_auth_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authenticated user identity",
        )

    return AuthIdentity(subject=x_auth_subject, email=x_auth_email)


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
