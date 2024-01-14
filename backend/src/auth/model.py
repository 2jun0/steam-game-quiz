from fastapi_users_db_sqlmodel import SQLModelBaseOAuthAccount, SQLModelBaseUserDB
from sqlmodel import Field, SQLModel

from ..model import CreatedAtMixin, UpdatedAtMixin


class OAuthAccount(CreatedAtMixin, UpdatedAtMixin, SQLModelBaseOAuthAccount, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")


class User(CreatedAtMixin, UpdatedAtMixin, SQLModelBaseUserDB, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=20)


class GuestUser(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__: str = "guest_account"

    id: int | None = Field(default=None, primary_key=True)
