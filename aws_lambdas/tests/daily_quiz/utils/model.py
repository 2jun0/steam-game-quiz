from datetime import datetime
from typing import Optional

from daily_quiz.aws_lambda.model import Game

from .utils import random_datetime

game_id_counter = 1


def create_random_game(
    *,
    steam_id: Optional[int] = None,
    name: Optional[str] = None,
    genres: Optional[list[str]] = None,
    aliases: list[str] = [],
    released_at: Optional[datetime] = None,
) -> Game:
    global game_id_counter
    game_id_counter += 1

    if steam_id is None:
        steam_id = game_id_counter
    if name is None:
        name = f"Game #{steam_id}"
    if genres is None:
        genres = [f"Genre #{steam_id}"]
    if released_at is None:
        released_at = random_datetime()

    created_at = datetime.utcnow()
    updated_at = datetime.utcnow()

    return Game(
        id=game_id_counter,
        steam_id=steam_id,
        name=name,
        created_at=created_at,
        updated_at=updated_at,
        genres=genres,
        aliases=aliases,
        released_at=released_at,
    )
