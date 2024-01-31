from typing import Any, AsyncGenerator

from fastapi import APIRouter, Depends, status
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin, models
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy, Strategy
from fastapi_users.openapi import OpenAPIResponseType

from ..config import settings
from .database import UserDBDep
from .model import User


class CustomFastAPIUsers(FastAPIUsers[models.UP, models.ID]):
    def get_logout_router(self, backend: AuthenticationBackend, requires_verification: bool = False) -> APIRouter:
        router = APIRouter()
        get_current_user_token = self.authenticator.current_user_token(active=True, verified=requires_verification)

        logout_responses: OpenAPIResponseType = {
            **{status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}},
            **backend.transport.get_openapi_logout_responses_success(),
        }

        @router.post("/logout", name=f"auth:{backend.name}.logout", responses=logout_responses)
        async def logout(
            user_token: tuple[models.UP, str] = Depends(get_current_user_token),
            strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
        ):
            user, token = user_token
            return await backend.logout(strategy, user, token)

        return router


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.JWT_SECRET
    verification_token_secret = settings.JWT_SECRET


async def get_user_manager(account_db: UserDBDep) -> AsyncGenerator[UserManager, Any]:
    yield UserManager(account_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=3600)


cookie_transport = CookieTransport()
auth_backend = AuthenticationBackend(name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy)
fastapi_users = CustomFastAPIUsers[User, int](get_user_manager, [auth_backend])
