from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from ..config import settings
from .model import Account


class AccountManager(IntegerIDMixin, BaseUserManager[Account, int]):
    reset_password_token_secret = settings.JWT_SECRET
    verification_token_secret = settings.JWT_SECRET

    async def on_after_register(self, account: Account, request: Request | None = None) -> None:
        ...


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=3600)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
auth_backend = AuthenticationBackend(name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy)
