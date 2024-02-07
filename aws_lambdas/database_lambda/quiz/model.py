from collections.abc import Sequence

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..model import Base, CreatedAtMixin, UpdatedAtMixin
from ..screenshot.model import GameScreenshot, GameScreenshotDto

quiz_screenshot_link = Table(
    "quiz_screenshot_link",
    Base.metadata,
    Column("id", type_=Integer, primary_key=True),
    Column("quiz_id", ForeignKey("quiz.id")),
    Column("screenshot_id", ForeignKey("game_screenshot.id")),
)


class Quiz(CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(primary_key=True)
    screenshots: Mapped[list[GameScreenshot]] = relationship(secondary=quiz_screenshot_link)

    def to_dto(self) -> "QuizDto":
        return QuizDto(id=self.id, screenshots=[s.to_dto() for s in self.screenshots])


class QuizDto(BaseModel):
    id: int
    screenshots: Sequence[GameScreenshotDto]
