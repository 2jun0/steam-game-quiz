from fastapi_users_db_sqlmodel import SQLModelBaseOAuthAccount, SQLModelBaseUserDB
from sqlmodel import Field, Relationship, SQLModel

from ..model import CreatedAtMixin, UpdatedAtMixin


class User(CreatedAtMixin, UpdatedAtMixin, SQLModelBaseUserDB, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=20)
    oauth_accounts: list["OAuthAccount"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "joined", "cascade": "all, delete"}
    )


class OAuthAccount(CreatedAtMixin, UpdatedAtMixin, SQLModelBaseOAuthAccount, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="oauth_accounts")


class Guest(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
