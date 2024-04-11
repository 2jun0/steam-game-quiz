from typing import Annotated

from fastapi import Depends

from ..dependency import SessionDep
from .model import User
from .repository import UserRepository
from .schema import UserRead
from .user import fastapi_users

current_active_user = fastapi_users.current_user(active=True)


async def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session=session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
CURRENT_USER_DEP = Annotated[User, Depends(current_active_user)]
CURRENT_READ_USER_DEP = Annotated[UserRead, Depends(current_active_user)]
