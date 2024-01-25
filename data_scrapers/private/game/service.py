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
    # turn to model
    models: dict[int, Game] = {}  # steam_id, Game
    for game in games:
        args = game.copy()
        args["genres"] = [_get_genres(session, genre_name) for genre_name in args["genres"]]
        args["released_at"] = datetime.fromtimestamp(args["released_at"])

        models[args["steam_id"]] = Game(**args)

    # detached된 객체의 식별자를 업데이트 함
    existeds = repository.get_games_in_steam_ids(session, [g["steam_id"] for g in games])
    for existed in existeds:
        query = models[existed.steam_id]
        existed.name = query.name
        existed.kr_name = query.kr_name
        existed.released_at = query.released_at
        existed.genres = query.genres

        models[existed.steam_id] = existed

    session.add_all(models.values())
    session.commit()


def get_games_in_steam_ids(session: Session, steam_ids: Sequence[int]) -> list[dict[str, Any]]:
    games = repository.get_games_in_steam_ids(session, steam_ids)

    return [g.to_dto().model_dump(mode="json") for g in games]
