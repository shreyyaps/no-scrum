from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from schemas.role import PermissionCreate, PermissionRead, RoleCreate, RoleRead
from services import role_service
from services.exceptions import ConflictError, NotFoundError
from utils.http_errors import raise_http_error

router = APIRouter()


@router.post("/roles", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_role(
    payload: RoleCreate,
    db: AsyncSession = Depends(get_db),
) -> RoleRead:
    return await role_service.create_role(db, payload)


@router.get("/roles/{role_id}", response_model=RoleRead)
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
) -> RoleRead:
    try:
        return await role_service.get_role(db, role_id)
    except NotFoundError as error:
        raise_http_error(error)


@router.post(
    "/permissions",
    response_model=PermissionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_permission(
    payload: PermissionCreate,
    db: AsyncSession = Depends(get_db),
) -> PermissionRead:
    return await role_service.create_permission(db, payload)


@router.post(
    "/roles/{role_id}/permissions/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    db: AsyncSession = Depends(get_db),
) -> Response:
    try:
        await role_service.assign_permission_to_role(db, role_id, permission_id)
    except (ConflictError, NotFoundError) as error:
        raise_http_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
