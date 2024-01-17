from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends
from fastapi_users.db.base import BaseUserDatabase
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync

from ..dependency import SessionDep
from .model import OAuthAccount, User


async def get_user_db(session: SessionDep) -> AsyncGenerator[SQLModelUserDatabaseAsync[User, int], Any]:
    yield SQLModelUserDatabaseAsync(session, User, OAuthAccount)


UserDBDep = Annotated[BaseUserDatabase, Depends(get_user_db)]
