from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..model import Base, CreatedAtMixin, UpdatedAtMixin


class Game(CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True)
    steam_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    kr_name: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"Game(id={self.id}, steam_id={self.steam_id}, name={self.name}, kr_name={self.kr_name})"


class GameScreenshot(CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "game_screenshot"

    id: Mapped[int] = mapped_column(primary_key=True)
    steam_file_id: Mapped[int] = mapped_column(unique=True)
    url: Mapped[str] = mapped_column(String(2048))

    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    game: Mapped[Game] = relationship()

    def __repr__(self) -> str:
        return (
            f"GameScreenshot(id={self.id}, url={self.url!r:100}, steam_file_id={self.steam_file_id!r:50},"
            f" game_id={self.game_id})"
        )
