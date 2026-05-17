from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    name: str


class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class PermissionCreate(BaseModel):
    name: str


class PermissionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
