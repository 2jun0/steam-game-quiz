from datetime import datetime
from typing import Any, Sequence

from sqlalchemy.orm import Session

from ..genre.repository import get_genre
from . import repository
from .model import Game


def get_some_games(session: Session) -> list[dict[str, Any]]:
    some_games = repository.get_all_games(session)

    return [g.to_dto().model_dump(mode="json") for g in some_games]


def save_games(session: Session, games: Sequence[dict[str, Any]]):
    for game in games:
        genres = []

        for genre_name in game["genres"]:
            genre = get_genre(session, name=genre_name)

            if genre is not None:
                genres.append(genre)

        del game["genres"]

        game["released_at"] = datetime.fromtimestamp(game["released_at"])

        session.add(Game(**game, genres=genres))


def get_games_in_steam_ids(session: Session, steam_ids: Sequence[int]) -> list[dict[str, Any]]:
    games = repository.get_games_in_steam_ids(session, steam_ids)

    return [g.to_dto().model_dump(mode="json") for g in games]
