from sqlmodel import Field, Relationship, SQLModel

from ..game.model import Game, GameScreenshot
from ..model import CreatedAtMixin, UpdatedAtMixin


class QuizScreenshotLink(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__: str = "quiz_screenshot_link"

    id: int | None = Field(default=None, primary_key=True)

    quiz_id: int = Field(foreign_key="quiz.id")
    screenshot_id: int = Field(foreign_key="game_screenshot.id")


class Quiz(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__: str = "quiz"

    id: int | None = Field(default=None, primary_key=True)

    screenshots: list[GameScreenshot] = Relationship(link_model=QuizScreenshotLink)

    @property
    def game(self) -> Game:
        return self.screenshots[0].game


class QuizSubmit(CreatedAtMixin, UpdatedAtMixin, SQLModel, table=True):
    __tablename__: str = "quiz_submit"

    id: int | None = Field(default=None, primary_key=True)

    answer: str = Field(max_length=64)
    correct: bool = Field()

    user_id: int = Field(foreign_key="user.id")
    quiz_id: int = Field(foreign_key="quiz.id")
    quiz: Quiz = Relationship()
