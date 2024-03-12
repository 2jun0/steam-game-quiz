from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..model import Base, CreatedAtMixin, UpdatedAtMixin


class GameAlias(CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "game_alias"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))

    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))

    def __repr__(self) -> str:
        return f"GameAlias(id={self.id}, name={self.name}, game_id={self.game_id}"

    def to_dto(self) -> "GameAliasDto":
        return GameAliasDto(
            id=self.id,
            name=self.name,
            game_id=self.game_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class GameAliasDto(BaseModel):
    id: int
    name: str
    game_id: int
    created_at: datetime
    updated_at: datetime
