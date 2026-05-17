from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    organization_id: int


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str


class UserRoleAssign(BaseModel):
    role_id: int
