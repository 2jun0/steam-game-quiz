from collections.abc import Iterable

from sqlalchemy.orm import Session

from .model_factory import to_models
from .schema import SaveQuiz


def save_quizzes(session: Session, quizzes: Iterable[SaveQuiz]):
    models = to_models(session, quizzes)
    session.add_all(models)
