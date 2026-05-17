from dataclasses import dataclass
from typing import Annotated

from fastapi import Header, HTTPException, status


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
