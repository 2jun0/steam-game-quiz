from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import Field, SQLModel

from ..model import CreatedAtMixin, UpdatedAtMixin


class Account(SQLModelBaseUserDB, CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__: str = "account"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=20)
    password: str | None = Field()


class GuestAccount(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__: str = "guest_account"

    id: int | None = Field(default=None, primary_key=True)
