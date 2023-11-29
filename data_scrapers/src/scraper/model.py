from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from ..model import CreatedAtMixin, UpdatedAtMixin


class Base(DeclarativeBase):
    pass


class Game(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True)
    steam_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    kr_name: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"Game(id={self.id}, steam_id={self.steam_id}, name={self.name}, kr_name={self.kr_name})"


class GameScreenshot(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "game_screenshot"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(2048))
    provider: Mapped[str] = mapped_column(String(256))

    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))
    game: Mapped[Game] = relationship()

    def __repr__(self) -> str:
        return f"GameScreenshot(id={self.id}, url={self.url!r:100}, provider={self.provider!r:50})"
