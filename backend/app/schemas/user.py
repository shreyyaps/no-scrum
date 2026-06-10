from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    organization_id: int
    name: str | None = None
    age: int | None = None


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str | None
    age: int | None


class UserRoleAssign(BaseModel):
    role_id: int
