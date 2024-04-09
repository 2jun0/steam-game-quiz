from asyncio import Lock

from sqlmodel.ext.asyncio.session import AsyncSession

from src.game.model import GameScreenshot

from .game import create_random_game
from .utils import random_image_url

steam_file_id_counter = 0
steam_file_id_lock = Lock()


async def create_random_game_screenshot(session: AsyncSession, *, game_id: int | None = None) -> GameScreenshot:
    global steam_file_id_counter

    if game_id is None:
        game = await create_random_game(session)
        assert game.id is not None
        game_id = game.id

    async with steam_file_id_lock:
        steam_file_id_counter += 1
        screenshot = GameScreenshot(steam_file_id=steam_file_id_counter, url=random_image_url(), game_id=game_id)

    session.add(screenshot)
    await session.commit()

    return screenshot
