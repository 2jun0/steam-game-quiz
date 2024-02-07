from collections.abc import Iterable

from sqlalchemy.orm import Session

from .exception import DuplicatedScreenshotsInQuizError
from .model_factory import to_models
from .schema import SaveQuiz


def save_quizzes(session: Session, quizzes: Iterable[SaveQuiz]):
    validate_duplicated_screenshots(quizzes)

    models = to_models(session, quizzes)
    session.add_all(models)


def validate_duplicated_screenshots(quizzes: Iterable[SaveQuiz]):
    for quiz in quizzes:
        screenshot_identities = [s["steam_file_id"] for s in quiz["screenshots"]]
        if len(set(screenshot_identities)) < len(screenshot_identities):
            raise DuplicatedScreenshotsInQuizError(f"중복된 스크린샷 식별자가 검출됨, 식별자: {screenshot_identities}")
