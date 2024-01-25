from datetime import datetime
from typing import Any, Sequence

from sqlalchemy.orm import Session

from ..genre.model import Genre
from ..genre.repository import get_genre
from . import repository
from .model import Game

genres: dict[str, Genre] = {}


def get_some_games(session: Session) -> list[dict[str, Any]]:
    some_games = repository.get_all_games(session)

    return [g.to_dto().model_dump(mode="json") for g in some_games]


def _get_genres(session: Session, name: str) -> Genre:
    if name not in genres:
        genre = get_genre(session, name=name)
        if genre is None:
            genre = Genre(name=name)
        genres[name] = genre

    return genres[name]


def save_games(session: Session, games: Sequence[dict[str, Any]]):
    for game in games:
        game_genres = []

        for genre_name in game["genres"]:
            game_genres.append(_get_genres(session, genre_name))

        game["genres"] = game_genres

        game["released_at"] = datetime.fromtimestamp(game["released_at"])

        session.add(Game(**game))


def get_games_in_steam_ids(session: Session, steam_ids: Sequence[int]) -> list[dict[str, Any]]:
    games = repository.get_games_in_steam_ids(session, steam_ids)

    return [g.to_dto().model_dump(mode="json") for g in games]
