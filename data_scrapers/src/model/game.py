from typing import Optional
from sqlmodel import Field, SQLModel
from .common import CreatedAtMixin, UpdatedAtMixin


class Game(SQLModel, CreatedAtMixin, UpdatedAtMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    steam_id: int = Field(unique=True)
    name: str = Field(max_length=64, nullable=False)
    kr_name: str = Field(max_length=64)
