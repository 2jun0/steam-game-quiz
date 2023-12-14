from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..game.model import Game
from ..model import Base, CreatedAtMixin, UpdatedAtMixin


class GameScreenshot(CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "game_screenshot"

    id: Mapped[int] = mapped_column(primary_key=True)
    steam_file_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    url: Mapped[str] = mapped_column(String(2048))

    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    game: Mapped[Game] = relationship()

    def __repr__(self) -> str:
        return (
            f"GameScreenshot(id={self.id}, url={self.url!r:100}, steam_file_id={self.steam_file_id!r:50},"
            f" game_id={self.game_id})"
        )
