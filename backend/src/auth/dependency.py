from typing import Annotated

from fastapi import Depends

from .schema import UserRead
from .user import fastapi_users

current_active_user = fastapi_users.current_user(active=True)

CURRENT_USER_DEP = Annotated[UserRead, Depends(current_active_user)]
