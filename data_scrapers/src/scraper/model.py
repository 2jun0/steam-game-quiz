from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from ..model import CreatedAtMixin, UpdatedAtMixin


class Game(SQLModel, CreatedAtMixin, UpdatedAtMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    steam_id: int = Field(unique=True)
    name: str = Field(max_length=64, nullable=False)
    kr_name: str = Field(max_length=64)


class GameScreenshot(SQLModel, CreatedAtMixin, UpdatedAtMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(max_length=2048, nullable=False)
    provider: str = Field(max_length=256)

    game_id: Optional[int] = Field(nullable=False)
    game: Optional[Game] = Relationship()
