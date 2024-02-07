from datetime import datetime
from random import randint
from typing import Optional

from sqlalchemy.orm import Session

from database_lambda.game.model import Game
from database_lambda.genre.model import Genre

from .genre import create_random_genre
from .utils import random_datetime

steam_id_counter = 0


def create_random_game(
    session: Session,
    *,
    name: Optional[str] = None,
    kr_name: Optional[str] = None,
    released_at: Optional[datetime] = None,
    genres: Optional[list[Genre]] = None,
) -> Game:
    global steam_id_counter
    steam_id_counter += 1

    if name is None:
        name = f"Game #{steam_id_counter}"
    if kr_name is None:
        kr_name = f"게임 #{steam_id_counter}"
    if released_at is None:
        released_at = random_datetime()
    if genres is None:
        genres = [create_random_genre(session) for _ in range(randint(0, 3))]

    game = Game(steam_id=steam_id_counter, name=name, kr_name=kr_name, genres=genres, released_at=released_at)

    session.add(game)
    session.commit()
    session.refresh(game)

    return game