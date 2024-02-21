from collections.abc import Sequence
from datetime import date

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Table
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


class DailyQuiz(CreatedAtMixin, UpdatedAtMixin, Base):
    __tablename__ = "daily_quiz"

    id: Mapped[int] = mapped_column(primary_key=True)
    target_date: Mapped[date] = mapped_column(nullable=False)

    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))
    quiz: Mapped[Quiz] = relationship()
    feature: Mapped[str] = mapped_column(String(64))

    def to_dto(self) -> "DailyQuizDto":
        return DailyQuizDto(id=self.id, target_date=self.target_date, quiz_id=self.quiz_id, quiz=self.quiz.to_dto())


class QuizDto(BaseModel):
    id: int
    screenshots: Sequence[GameScreenshotDto]


class DailyQuizDto(BaseModel):
    id: int
    target_date: date
    quiz_id: int
    quiz: QuizDto
