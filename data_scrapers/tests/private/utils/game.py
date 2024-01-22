from random import randint, randrange
from typing import Optional

from sqlalchemy.orm import Session

from private.game.model import Game
from private.genre.model import Genre

from .genre import create_random_genre

steam_id_counter = 0


def create_random_game(
    session: Session,
    *,
    name: Optional[str] = None,
    kr_name: Optional[str] = None,
    owners: Optional[int] = None,
    genres: Optional[list[Genre]] = None,
) -> Game:
    global steam_id_counter
    steam_id_counter += 1

    if name is None:
        name = f"Game #{steam_id_counter}"
    if kr_name is None:
        kr_name = f"게임 #{steam_id_counter}"
    if owners is None:
        owners = randrange(0, 1000000, 10000)
    if genres is None:
        genres = [create_random_genre(session) for _ in range(randint(0, 3))]

    game = Game(steam_id=steam_id_counter, name=name, kr_name=kr_name, genres=genres, owners=owners)

    session.add(game)
    session.commit()
    session.refresh(game)

    return game
