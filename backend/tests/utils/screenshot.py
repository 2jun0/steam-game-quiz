from asyncio import Lock

from sqlmodel import Session

from src.database import engine
from src.game.model import GameScreenshot

from .game import create_random_game
from .utils import random_image_url

steam_file_id_counter = 0
steam_file_id_lock = Lock()


async def create_random_game_screenshot(game_id: int | None) -> GameScreenshot:
    global steam_file_id_counter

    if game_id is None:
        game = await create_random_game()
        game_id = game.id

    with Session(engine) as session:
        async with steam_file_id_lock:
            steam_file_id_counter += 1
            screenshot = GameScreenshot(steam_file_id=steam_file_id_counter, url=random_image_url(), game_id=game_id)

        session.add(screenshot)
        session.commit()
        session.refresh(screenshot)

    return screenshot
