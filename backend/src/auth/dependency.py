from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends
from fastapi_users import BaseUserManager
from fastapi_users.db.base import BaseUserDatabase
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync

from ..dependency import SessionDep
from .model import OAuthAccount, User
from .user import UserManager


async def get_user_db(session: SessionDep) -> AsyncGenerator[SQLModelUserDatabaseAsync[User, int], Any]:
    yield SQLModelUserDatabaseAsync(session, User, OAuthAccount)


async def get_user_manager(account_db: "UserDBDep") -> AsyncGenerator[UserManager, Any]:
    yield UserManager(account_db)


UserDBDep = Annotated[BaseUserDatabase, Depends(get_user_db)]
UserManagerDep = Annotated[BaseUserManager, Depends(get_user_manager)]
