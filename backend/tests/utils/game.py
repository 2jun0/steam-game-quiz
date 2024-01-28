from datetime import datetime
from threading import Lock

from sqlmodel import Session

from src.game.model import Game

from .utils import random_datetime, random_kr_string, random_name

steam_id_counter = 0
steam_id_lock = Lock()


def create_random_game(
    session: Session, *, name: str | None = None, kr_name: str | None = None, released_at: datetime | None = None
) -> Game:
    global steam_id_counter

    if name is None:
        name = random_name()
    if kr_name is None:
        kr_name = random_kr_string()
    if released_at is None:
        released_at = random_datetime()

    with steam_id_lock:
        steam_id_counter += 1
        game = Game(steam_id=steam_id_counter, name=name, kr_name=kr_name, released_at=released_at)

    session.add(game)
    session.commit()
    session.refresh(game)

    return game
