from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from models.user_roles import user_roles


async def create(
    db: AsyncSession,
    email: str,
    name: str | None = None,
    age: int | None = None,
) -> User:
    user = User(email=email, name=name, age=age)
    db.add(user)
    await db.flush()
    return user


async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)


async def get_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def role_link_exists(
    db: AsyncSession,
    user_id: int,
    role_id: int,
) -> bool:
    result = await db.execute(
        select(user_roles).where(
            user_roles.c.user_id == user_id,
            user_roles.c.role_id == role_id,
        )
    )
    return result.first() is not None


async def add_role(db: AsyncSession, user_id: int, role_id: int) -> None:
    await db.execute(user_roles.insert().values(user_id=user_id, role_id=role_id))
