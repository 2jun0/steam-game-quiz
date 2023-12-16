from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..model import Base, CreatedAtMixin, UpdatedAtMixin


class Game(CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True)
    steam_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(64))
    kr_name: Mapped[Optional[str]] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"Game(id={self.id}, steam_id={self.steam_id}, name={self.name}, kr_name={self.kr_name})"

    def to_dto(self) -> "GameDto":
        return GameDto(
            id=self.id,
            steam_id=self.steam_id,
            name=self.name,
            kr_name=self.kr_name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class GameDto(BaseModel):
    id: int
    steam_id: int
    name: str
    kr_name: Optional[str]
    created_at: datetime
    updated_at: datetime
