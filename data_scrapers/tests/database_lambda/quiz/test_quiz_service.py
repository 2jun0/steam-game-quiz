from sqlalchemy import select
from sqlalchemy.orm import Session

from database_lambda.quiz.model import Quiz
from database_lambda.quiz.schema import SaveQuiz
from database_lambda.quiz.service import save_quizzes
from tests.database_lambda.utils.game import create_random_game


def test_save_quizzes은_입력한_퀴즈를_저장해야_한다(session: Session):
    saved_games = [create_random_game(session) for _ in range(2)]
    quizzes: list[SaveQuiz] = [
        {
            "screenshots": [
                {"steam_file_id": 1, "url": "https://fake.url/1", "game_id": saved_games[0].id},
                {"steam_file_id": 2, "url": "https://fake.url/2", "game_id": saved_games[0].id},
                {"steam_file_id": 3, "url": "https://fake.url/3", "game_id": saved_games[0].id},
                {"steam_file_id": 4, "url": "https://fake.url/4", "game_id": saved_games[0].id},
                {"steam_file_id": 5, "url": "https://fake.url/5", "game_id": saved_games[0].id},
            ]
        },
        {
            "screenshots": [
                {"steam_file_id": 6, "url": "https://fake.url/6", "game_id": saved_games[1].id},
                {"steam_file_id": 7, "url": "https://fake.url/7", "game_id": saved_games[1].id},
                {"steam_file_id": 8, "url": "https://fake.url/8", "game_id": saved_games[1].id},
                {"steam_file_id": 9, "url": "https://fake.url/9", "game_id": saved_games[1].id},
                {"steam_file_id": 10, "url": "https://fake.url/10", "game_id": saved_games[1].id},
            ]
        },
    ]

    save_quizzes(session, quizzes)

    saved = session.scalars(select(Quiz)).all()
    assert len(saved) == 2


def test_save_quizzes은_입력한_퀴즈내_스크린샷을_저장해야_한다(session: Session):
    saved_games = [create_random_game(session) for _ in range(2)]
    quizzes: list[SaveQuiz] = [
        {
            "screenshots": [
                {"steam_file_id": 1, "url": "https://fake.url/1", "game_id": saved_games[0].id},
                {"steam_file_id": 2, "url": "https://fake.url/2", "game_id": saved_games[0].id},
                {"steam_file_id": 3, "url": "https://fake.url/3", "game_id": saved_games[0].id},
                {"steam_file_id": 4, "url": "https://fake.url/4", "game_id": saved_games[0].id},
                {"steam_file_id": 5, "url": "https://fake.url/5", "game_id": saved_games[0].id},
            ]
        },
        {
            "screenshots": [
                {"steam_file_id": 6, "url": "https://fake.url/6", "game_id": saved_games[1].id},
                {"steam_file_id": 7, "url": "https://fake.url/7", "game_id": saved_games[1].id},
                {"steam_file_id": 8, "url": "https://fake.url/8", "game_id": saved_games[1].id},
                {"steam_file_id": 9, "url": "https://fake.url/9", "game_id": saved_games[1].id},
                {"steam_file_id": 10, "url": "https://fake.url/10", "game_id": saved_games[1].id},
            ]
        },
    ]

    save_quizzes(session, quizzes)

    saved = session.scalars(select(Quiz)).all()
    for saved_q, q in zip(saved, quizzes):
        saved_screenshots = sorted(saved_q.screenshots, key=lambda s: s.steam_file_id)
        screenshots = sorted(q["screenshots"], key=lambda s: s["steam_file_id"])

        for saved_s, s in zip(saved_screenshots, screenshots):
            assert saved_s.steam_file_id == s["steam_file_id"]
            assert saved_s.game_id == s["game_id"]
            assert saved_s.url == s["url"]
