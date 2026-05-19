from fastapi import APIRouter

from api.v1 import health, organizations, roles, users

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    organizations.router,
    prefix="/organizations",
    tags=["organizations"],
)
api_router.include_router(roles.router, tags=["roles"])
