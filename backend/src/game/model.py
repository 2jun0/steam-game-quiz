from datetime import datetime

from sqlalchemy import BigInteger, Column, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

from ..model import CreatedAtMixin, UpdatedAtMixin

# Genre


class GameGenreLink(SQLModel, table=True):
    __tablename__: str = "game_genre_link"
    __table_args__ = (UniqueConstraint("game_id", "genre_id"),)

    id: int | None = Field(default=None, primary_key=True)

    game_id: int = Field(foreign_key="game.id")
    genre_id: int = Field(foreign_key="genre.id")


class Genre(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__: str = "genre"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=64, unique=True)


# Game


class Game(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__: str = "game"

    id: int | None = Field(default=None, primary_key=True)
    steam_id: int = Field(unique=True)
    name: str = Field(max_length=64)
    released_at: datetime = Field()
    genres: list[Genre] = Relationship(link_model=GameGenreLink)
    aliases: list["GameAlias"] = Relationship(sa_relationship_kwargs={"cascade": "all,delete-orphan"})


# Game Alias


class GameAlias(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__: str = "game_alias"
    __table_args__ = (UniqueConstraint("game_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=64)

    game_id: int | None = Field(default=None, foreign_key="game.id")


# Screenshot


class GameScreenshot(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__: str = "game_screenshot"

    id: int | None = Field(default=None, primary_key=True)
    steam_file_id: int = Field(sa_column=Column(BigInteger(), unique=True))
    url: str = Field(max_length=2048)

    game_id: int = Field(foreign_key="game.id")
    game: Game = Relationship()
