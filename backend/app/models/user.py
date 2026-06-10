from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.session import Base
from models.user_roles import user_roles

if TYPE_CHECKING:
    from models.organization_user import OrganizationUser
    from models.role import Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)

    organization_membership: Mapped["OrganizationUser | None"] = relationship(
        "OrganizationUser",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
    )
