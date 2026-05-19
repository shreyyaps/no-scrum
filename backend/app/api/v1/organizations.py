from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from schemas.organization import (
    OrganizationCreate,
    OrganizationRead,
    OrganizationUserRead,
)
from services import org_service
from services.exceptions import ConflictError, NotFoundError
from utils.http_errors import raise_http_error

router = APIRouter()


@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
) -> OrganizationRead:
    return await org_service.create_organization(db, payload)


@router.get("/{organization_id}", response_model=OrganizationRead)
async def get_organization(
    organization_id: int,
    db: AsyncSession = Depends(get_db),
) -> OrganizationRead:
    try:
        return await org_service.get_organization(db, organization_id)
    except NotFoundError as error:
        raise_http_error(error)


@router.post(
    "/{organization_id}/users/{user_id}",
    response_model=OrganizationUserRead,
    status_code=status.HTTP_201_CREATED,
)
async def assign_user_to_organization(
    organization_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> OrganizationUserRead:
    try:
        return await org_service.assign_user_to_organization(
            db=db,
            user_id=user_id,
            organization_id=organization_id,
        )
    except (ConflictError, NotFoundError) as error:
        raise_http_error(error)


@router.get("/{organization_id}/users", response_model=list[OrganizationUserRead])
async def list_organization_users(
    organization_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[OrganizationUserRead]:
    try:
        return await org_service.list_organization_users(db, organization_id)
    except NotFoundError as error:
        raise_http_error(error)
