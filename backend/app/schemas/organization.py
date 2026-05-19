from pydantic import BaseModel, ConfigDict


class OrganizationCreate(BaseModel):
    name: str


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class OrganizationUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    organization_id: int
