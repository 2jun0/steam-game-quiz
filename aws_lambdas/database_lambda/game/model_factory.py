from collections.abc import Iterable
from datetime import datetime

from sqlalchemy.orm import Session

from ..genre.model_factory import to_models as to_genre_models
from . import repository
from .model import Game
from .schema import STEAM_ID, SaveGame


def _create_model(session: Session, game: SaveGame) -> Game:
    return Game(
        steam_id=game["steam_id"],
        name=game["name"],
        kr_name=game["kr_name"],
        released_at=datetime.fromtimestamp(game["released_at"]),
        genres=to_genre_models(session, game["genres"]),
    )


def _create_models(session: Session, games: Iterable[SaveGame]) -> dict[STEAM_ID, Game]:
    models: dict[STEAM_ID, Game] = {}
    for game in games:
        models[game["steam_id"]] = _create_model(session, game)

    return models


def _attach_models(session: Session, models: dict[STEAM_ID, Game]):
    saved = repository.get_games_in_steam_ids(session, models.keys())

    for game in saved:
        query = models[game.steam_id]
        game.name = query.name
        game.kr_name = query.kr_name
        models[game.steam_id] = game


def to_models(session: Session, games: Iterable[SaveGame]) -> list[Game]:
    models = _create_models(session, games)
    _attach_models(session, models)

    return list(models.values())
