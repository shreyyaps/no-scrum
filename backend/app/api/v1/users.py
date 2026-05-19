from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from schemas.user import UserCreate, UserRead
from services import user_service
from services.exceptions import ConflictError, NotFoundError
from utils.http_errors import raise_http_error

router = APIRouter()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    try:
        return await user_service.create_user(db, payload)
    except (ConflictError, NotFoundError) as error:
        raise_http_error(error)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    try:
        return await user_service.get_user(db, user_id)
    except NotFoundError as error:
        raise_http_error(error)


@router.post("/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    db: AsyncSession = Depends(get_db),
) -> Response:
    try:
        await user_service.assign_role_to_user(db, user_id, role_id)
    except (ConflictError, NotFoundError) as error:
        raise_http_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{user_id}/permissions", response_model=list[str])
async def get_user_permissions(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> list[str]:
    try:
        return await user_service.get_user_permission_names(db, user_id)
    except NotFoundError as error:
        raise_http_error(error)
