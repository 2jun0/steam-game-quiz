from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.model import User

from .utils import random_email


async def create_random_user(
    session: AsyncSession,
    *,
    email: str | None = None,
    is_active: bool = True,
    is_superuser: bool = False,
    is_verified: bool = False
) -> User:
    if email is None:
        email = random_email()

    user = User(
        email=email,
        hashed_password="hashed_password",
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )

    session.add(user)
    await session.commit()

    return user
