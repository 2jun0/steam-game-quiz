import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from database_lambda.quiz.exception import DuplicatedScreenshotsInQuizError, MultipleGamesInQuizError
from database_lambda.quiz.model import DailyQuiz
from database_lambda.quiz.schema import SaveDailyQuiz
from database_lambda.quiz.service import save_daily_quizzes
from tests.database_lambda.utils.game import create_random_game
from tests.database_lambda.utils.quiz import create_random_feature


def test_save_daily_quizzes은_입력한_데일리_퀴즈를_저장해야_한다(session: Session):
    saved_games = [create_random_game(session) for _ in range(2)]
    daily_quiz: SaveDailyQuiz = {
        "target_date": "2023-1-10",
        "quiz": {
            "screenshots": [
                {"steam_file_id": 1, "url": "https://fake.url/1", "game_id": saved_games[0].id},
                {"steam_file_id": 2, "url": "https://fake.url/2", "game_id": saved_games[0].id},
                {"steam_file_id": 3, "url": "https://fake.url/3", "game_id": saved_games[0].id},
                {"steam_file_id": 4, "url": "https://fake.url/4", "game_id": saved_games[0].id},
                {"steam_file_id": 5, "url": "https://fake.url/5", "game_id": saved_games[0].id},
            ]
        },
        "feature": create_random_feature(),
    }

    save_daily_quizzes([daily_quiz], session=session)

    saved = session.scalars(select(DailyQuiz)).one()
    assert saved.feature == daily_quiz["feature"]


def test_save_daily_quizzes은_입력한_여러개의_데일리_퀴즈를_저장해야_한다(session: Session):
    saved_games = [create_random_game(session) for _ in range(2)]
    daily_quizzes: list[SaveDailyQuiz] = [
        {
            "target_date": "2023-1-10",
            "quiz": {
                "screenshots": [
                    {"steam_file_id": 1, "url": "https://fake.url/1", "game_id": saved_games[0].id},
                    {"steam_file_id": 2, "url": "https://fake.url/2", "game_id": saved_games[0].id},
                    {"steam_file_id": 3, "url": "https://fake.url/3", "game_id": saved_games[0].id},
                    {"steam_file_id": 4, "url": "https://fake.url/4", "game_id": saved_games[0].id},
                    {"steam_file_id": 5, "url": "https://fake.url/5", "game_id": saved_games[0].id},
                ]
            },
            "feature": create_random_feature(),
        },
        {
            "target_date": "2023-1-10",
            "quiz": {
                "screenshots": [
                    {"steam_file_id": 6, "url": "https://fake.url/6", "game_id": saved_games[1].id},
                    {"steam_file_id": 7, "url": "https://fake.url/7", "game_id": saved_games[1].id},
                    {"steam_file_id": 8, "url": "https://fake.url/8", "game_id": saved_games[1].id},
                    {"steam_file_id": 9, "url": "https://fake.url/9", "game_id": saved_games[1].id},
                    {"steam_file_id": 10, "url": "https://fake.url/10", "game_id": saved_games[1].id},
                ]
            },
            "feature": create_random_feature(),
        },
    ]

    save_daily_quizzes(daily_quizzes, session=session)

    saved = session.scalars(select(DailyQuiz)).all()
    assert len(saved) == 2


def test_save_daily_quizzes은_한_퀴즈에_여러개의_게임_스크린샷이_있으면_예외를_던져야_한다(session: Session):
    saved_games = [create_random_game(session) for _ in range(2)]
    daily_quizzes: list[SaveDailyQuiz] = [
        {
            "target_date": "2023-1-10",
            "quiz": {
                "screenshots": [
                    {"steam_file_id": 1, "url": "https://fake.url/1", "game_id": saved_games[0].id},
                    {"steam_file_id": 2, "url": "https://fake.url/2", "game_id": saved_games[0].id},
                    {"steam_file_id": 3, "url": "https://fake.url/3", "game_id": saved_games[1].id},
                    {"steam_file_id": 4, "url": "https://fake.url/4", "game_id": saved_games[1].id},
                    {"steam_file_id": 5, "url": "https://fake.url/5", "game_id": saved_games[1].id},
                ]
            },
            "feature": create_random_feature(),
        }
    ]

    with pytest.raises(MultipleGamesInQuizError):
        save_daily_quizzes(daily_quizzes, session=session)


def test_save_daily_quizzes은_한_퀴즈에_중복된_스크린샷이_있으면_예외를_던져야_한다(session: Session):
    saved_games = [create_random_game(session) for _ in range(2)]
    daily_quizzes: list[SaveDailyQuiz] = [
        {
            "target_date": "2023-1-10",
            "quiz": {
                "screenshots": [
                    {"steam_file_id": 1, "url": "https://fake.url/1", "game_id": saved_games[0].id},
                    {"steam_file_id": 1, "url": "https://fake.url/1", "game_id": saved_games[0].id},
                    {"steam_file_id": 3, "url": "https://fake.url/3", "game_id": saved_games[0].id},
                    {"steam_file_id": 4, "url": "https://fake.url/4", "game_id": saved_games[0].id},
                    {"steam_file_id": 5, "url": "https://fake.url/5", "game_id": saved_games[0].id},
                ]
            },
            "feature": create_random_feature(),
        }
    ]

    with pytest.raises(DuplicatedScreenshotsInQuizError):
        save_daily_quizzes(daily_quizzes, session=session)
