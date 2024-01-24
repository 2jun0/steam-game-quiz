from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..genre.model import Genre
from ..model import Base, CreatedAtMixin, UpdatedAtMixin

game_genre_link = Table(
    "game_genre_link",
    Base.metadata,
    Column("id", type_=Integer, primary_key=True),
    Column("game_id", ForeignKey("game.id")),
    Column("genre_id", ForeignKey("genre.id")),
)


class Game(CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True)
    steam_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(64))
    kr_name: Mapped[Optional[str]] = mapped_column(String(64))
    released_at: Mapped[datetime] = mapped_column()
    genres: Mapped[list[Genre]] = relationship(secondary=game_genre_link)

    def __repr__(self) -> str:
        return (
            f"Game(id={self.id}, steam_id={self.steam_id}, name={self.name}, kr_name={self.kr_name},"
            f" released_at={self.released_at})"
        )

    def to_dto(self) -> "GameDto":
        return GameDto(
            id=self.id,
            steam_id=self.steam_id,
            name=self.name,
            kr_name=self.kr_name,
            released_at=self.released_at,
            genres=[g.name for g in self.genres],
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class GameDto(BaseModel):
    id: int
    steam_id: int
    name: str
    kr_name: Optional[str]
    released_at: datetime
    genres: list[str]
    created_at: datetime
    updated_at: datetime
