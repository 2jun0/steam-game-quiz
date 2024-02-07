from collections.abc import Iterable

from sqlalchemy.orm import Session

from .exception import DuplicatedScreenshotsInQuizError, MultipleGamesInQuizError
from .model_factory import to_models
from .schema import SaveQuiz


def save_quizzes(session: Session, quizzes: Iterable[SaveQuiz]):
    for quiz in quizzes:
        validate_duplicated_screenshots(quiz)
        validate_multiple_games(quiz)

    models = to_models(session, quizzes)
    session.add_all(models)


def validate_duplicated_screenshots(quiz: SaveQuiz):
    screenshot_identities = [s["steam_file_id"] for s in quiz["screenshots"]]
    if len(set(screenshot_identities)) < len(screenshot_identities):
        raise DuplicatedScreenshotsInQuizError(f"중복된 스크린샷 식별자가 검출됨, 식별자: {screenshot_identities}")


def validate_multiple_games(quiz: SaveQuiz):
    game_ids = [s["game_id"] for s in quiz["screenshots"]]
    if len(set(game_ids)) > 1:
        raise MultipleGamesInQuizError(f"한 퀴즈내에 여러개의 게임이 검출됨, 게임 id: {game_ids}")
