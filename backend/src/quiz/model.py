from sqlmodel import Field, Relationship, SQLModel

from ..model import CreatedAtMixin, UpdatedAtMixin
from ..game.model import GameScreenshot


class QuizScreenshotLink(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__ = "quiz_screenshot_link"

    id: int | None = Field(default=None, primary_key=True)

    quiz_id: int = Field(foreign_key="quiz.id")
    screenshot_id: int = Field(foreign_key="game_screenshot.id")


class Quiz(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__ = "quiz"

    id: int | None = Field(default=None, primary_key=True)

    screenshots: list[GameScreenshot] = Relationship(back_populates="game_screenshot", link_model=QuizScreenshotLink)
