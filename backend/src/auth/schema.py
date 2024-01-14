from fastapi_users import schemas


class AccountRead(schemas.BaseUser[int]):
    pass


class AccountCreate(schemas.BaseUserCreate):
    pass


class AccountUpdate(schemas.BaseUserUpdate):
    pass
