from pydantic import BaseModel, ConfigDict


class OrganizationCreate(BaseModel):
    name: str
    description: str | None = None


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None


class OrganizationUserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    organization_id: int
