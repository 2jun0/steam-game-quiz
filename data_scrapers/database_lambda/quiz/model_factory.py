from collections.abc import Iterable

from sqlalchemy.orm import Session

from ..screenshot import model_factory as screenshot_model_factory
from .model import Quiz
from .schema import SaveQuiz


def to_models(session: Session, quizzes: Iterable[SaveQuiz]) -> list[Quiz]:
    models: list[Quiz] = []
    for quiz in quizzes:
        screenshot_models = screenshot_model_factory.to_models(session, screenshots=quiz["screenshots"])
        models.append(Quiz(screenshots=screenshot_models))

    return models
