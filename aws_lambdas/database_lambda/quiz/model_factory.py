from collections.abc import Iterable
from datetime import datetime

from sqlalchemy.orm import Session

from ..screenshot import model_factory as screenshot_model_factory
from .model import DailyQuiz, Quiz
from .schema import SaveDailyQuiz, SaveQuiz


def to_quiz_model(session: Session, quiz: SaveQuiz) -> Quiz:
    screenshot_models = screenshot_model_factory.to_models(session, screenshots=quiz["screenshots"])
    return Quiz(screenshots=screenshot_models)


def to_quiz_models(session: Session, quizzes: Iterable[SaveQuiz]) -> list[Quiz]:
    return [to_quiz_model(session, quiz) for quiz in quizzes]


def to_daily_quiz_model(session: Session, daily_quiz: SaveDailyQuiz) -> DailyQuiz:
    quiz_model = to_quiz_model(session, daily_quiz["quiz"])
    target_date = datetime.strptime(daily_quiz["target_date"], "%Y-%m-%d").date()
    return DailyQuiz(target_date=target_date, quiz=quiz_model)


def to_daily_quiz_models(session: Session, daily_quizzes: Iterable[SaveDailyQuiz]) -> list[DailyQuiz]:
    return [to_daily_quiz_model(session, daily_quiz) for daily_quiz in daily_quizzes]
