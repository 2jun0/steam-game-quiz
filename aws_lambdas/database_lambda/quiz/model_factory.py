from collections.abc import Iterable

from sqlalchemy.orm import Session

from ..screenshot import model_factory as screenshot_model_factory
from .model import Quiz
from .schema import SaveQuiz


def to_model(session: Session, quiz: SaveQuiz) -> Quiz:
    screenshot_models = screenshot_model_factory.to_models(session, screenshots=quiz["screenshots"])
    return Quiz(screenshots=screenshot_models)


def to_models(session: Session, quizzes: Iterable[SaveQuiz]) -> list[Quiz]:
    return [to_model(session, quiz) for quiz in quizzes]
