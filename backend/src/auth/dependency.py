from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends
from fastapi_users import BaseUserManager
from fastapi_users.db.base import BaseUserDatabase
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync

from ..dependency import SessionDep
from .account import AccountManager
from .model import Account


async def get_account_db(session: SessionDep) -> AsyncGenerator[SQLModelUserDatabaseAsync[Account, int], Any]:
    yield SQLModelUserDatabaseAsync(session, Account)


async def get_account_manager(account_db: "AccountDBDep") -> AsyncGenerator[AccountManager, Any]:
    yield AccountManager(account_db)


AccountDBDep = Annotated[BaseUserDatabase, Depends(get_account_db)]
AccountManagerDep = Annotated[BaseUserManager, Depends(get_account_manager)]
