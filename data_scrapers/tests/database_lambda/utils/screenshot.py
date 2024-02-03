from typing import Optional

from sqlalchemy.orm import Session

from database_lambda.screenshot.model import GameScreenshot

from .game import create_random_game

steam_file_id_counter = 0


def create_random_game_screenshot(session: Session, *, game_id: Optional[int] = None) -> GameScreenshot:
    global steam_file_id_counter
    steam_file_id_counter += 1

    if game_id is None:
        game = create_random_game(session)
        game_id = game.id

    screenshot = GameScreenshot(
        steam_file_id=steam_file_id_counter, url=f"http://example.com/url/{steam_file_id_counter}", game_id=game_id
    )

    session.add(screenshot)
    session.commit()
    session.refresh(screenshot)

    return screenshot
