from sqlalchemy import BigInteger, Column
from sqlmodel import Field, Relationship, SQLModel

from model import CreatedAtMixin, UpdatedAtMixin


class Game(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__ = "game"

    id: int | None = Field(default=None, primary_key=True)
    steam_id: int = Field(unique=True)
    name: str = Field(max_length=64)
    kr_name: str | None = Field(max_length=64)


class GameScreenshot(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__ = "game_screenshot"

    id: int | None = Field(default=None, primary_key=True)
    steam_file_id: int = Field(sa_column=Column(BigInteger(), unique=True))
    url: str = Field(max_length=2048)

    game_id: int = Field(foreign_key="game.id")
    game: Game = Relationship()
