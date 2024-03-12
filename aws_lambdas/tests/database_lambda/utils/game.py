from datetime import datetime
from random import randint
from typing import Any, Optional

from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session

from database_lambda.es import GAME_INDEX
from database_lambda.game.model import Game
from database_lambda.genre.model import Genre
from database_lambda.alias.model import GameAlias

from .genre import create_random_genre
from .utils import random_datetime

steam_id_counter = 0


def create_random_game(
    session: Session,
    *,
    name: Optional[str] = None,
    released_at: Optional[datetime] = None,
    genres: Optional[list[Genre]] = None,
    aliases: Optional[list[str]] = None,
) -> Game:
    global steam_id_counter
    steam_id_counter += 1

    if name is None:
        name = f"Game #{steam_id_counter}"
    if released_at is None:
        released_at = random_datetime()
    if genres is None:
        genres = [create_random_genre(session) for _ in range(randint(0, 3))]
    if aliases is None:
        aliases = ["Alias #1", "Alias #2", "Alias #3"]

    game = Game(
        steam_id=steam_id_counter,
        name=name,
        genres=genres,
        aliases=[GameAlias(name=alias) for alias in aliases],
        released_at=released_at,
    )

    session.add(game)
    session.commit()
    session.refresh(game)

    return game


def search_game_docs(es_client: Elasticsearch, *, max_size: int = 100) -> list[dict[str, Any]]:
    return es_client.search(index=GAME_INDEX, size=max_size)["hits"]["hits"]
