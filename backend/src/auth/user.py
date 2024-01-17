from typing import Any, AsyncGenerator

from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from ..config import settings
from .database import UserDBDep
from .model import User


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.JWT_SECRET
    verification_token_secret = settings.JWT_SECRET


async def get_user_manager(account_db: UserDBDep) -> AsyncGenerator[UserManager, Any]:
    yield UserManager(account_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=3600)


cookie_transport = CookieTransport()
auth_backend = AuthenticationBackend(name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy)
fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
