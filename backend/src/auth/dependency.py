from typing import Annotated

from fastapi import Depends

from .model import User
from .user import fastapi_users

current_active_verified_user = fastapi_users.current_user(active=True, verified=True)

CURRENT_USER_DEP = Annotated[User, Depends(current_active_verified_user)]
