from asyncio import Lock

from sqlmodel import Session

from src.database import engine
from src.game.model import Game

from .utils import random_kr_string, random_name

steam_id_counter = 0
steam_id_lock = Lock()


async def create_random_game() -> Game:
    global steam_id_counter

    with Session(engine) as session:
        async with steam_id_lock:
            steam_id_counter += 1
            game = Game(steam_id=steam_id_counter, name=random_name(), kr_name=random_kr_string())

        session.add(game)
        session.commit()
        session.refresh(game)

    return game
