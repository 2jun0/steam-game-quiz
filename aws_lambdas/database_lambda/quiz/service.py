from collections.abc import Iterable

from sqlalchemy.orm import Session

from .exception import DuplicatedScreenshotsInQuizError, MultipleGamesInQuizError
from .model_factory import to_daily_quiz_models, to_quiz_models
from .schema import SaveDailyQuiz, SaveQuiz


def _validate_duplicated_screenshots(quiz: SaveQuiz):
    screenshot_identities = [s["steam_file_id"] for s in quiz["screenshots"]]
    if len(set(screenshot_identities)) < len(screenshot_identities):
        raise DuplicatedScreenshotsInQuizError(f"중복된 스크린샷 식별자가 검출됨, 식별자: {screenshot_identities}")


def _validate_multiple_games(quiz: SaveQuiz):
    game_ids = [s["game_id"] for s in quiz["screenshots"]]
    if len(set(game_ids)) > 1:
        raise MultipleGamesInQuizError(f"한 퀴즈내에 여러개의 게임이 검출됨, 게임 id: {game_ids}")


def save_quizzes(quizzes: Iterable[SaveQuiz], *, session: Session, **kwargs):
    for quiz in quizzes:
        _validate_duplicated_screenshots(quiz)
        _validate_multiple_games(quiz)

    models = to_quiz_models(session, quizzes)
    session.add_all(models)


def save_daily_quizzes(daily_quizzes: Iterable[SaveDailyQuiz], *, session: Session, **kwargs):
    for daily_quiz in daily_quizzes:
        _validate_duplicated_screenshots(daily_quiz["quiz"])
        _validate_multiple_games(daily_quiz["quiz"])

    models = to_daily_quiz_models(session, daily_quizzes)
    session.add_all(models)
