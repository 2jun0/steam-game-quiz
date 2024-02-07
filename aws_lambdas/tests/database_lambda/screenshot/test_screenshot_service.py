from sqlalchemy import select
from sqlalchemy.orm import Session

from database_lambda.screenshot.model import GameScreenshot
from database_lambda.screenshot.service import SaveGameScreenshot, save_screenshots
from tests.database_lambda.utils.game import create_random_game


def test_save_screenshots은_입력한_스크린샷을_저장해야_한다(session: Session):
    saved_games = [create_random_game(session) for _ in range(2)]

    screenshots: list[SaveGameScreenshot] = [
        {"steam_file_id": 1, "url": "https://fake.url/1", "game_id": saved_games[0].id},
        {"steam_file_id": 2, "url": "https://fake.url/2", "game_id": saved_games[0].id},
        {"steam_file_id": 3, "url": "https://fake.url/3", "game_id": saved_games[1].id},
        {"steam_file_id": 4, "url": "https://fake.url/4", "game_id": saved_games[1].id},
    ]
    save_screenshots(session, screenshots)

    saved = session.scalars(select(GameScreenshot)).all()
    assert len(saved) == 4


def test_save_screenshots은_이미_저장한_스크린샷은_업데이트_한다(session: Session):
    saved_games = [create_random_game(session) for _ in range(2)]

    before: SaveGameScreenshot = {"steam_file_id": 1, "url": "https://fake.url/1", "game_id": saved_games[0].id}
    after: SaveGameScreenshot = {"steam_file_id": 1, "url": "https://fake.url/1a", "game_id": saved_games[0].id}

    save_screenshots(session, [before])
    save_screenshots(session, [after])
    saved = session.scalars(select(GameScreenshot)).one()

    assert saved.steam_file_id == after["steam_file_id"]
    assert saved.url == after["url"]
