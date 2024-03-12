from collections.abc import Iterable
from datetime import datetime

from sqlalchemy.orm import Session

from ..alias.model import GameAlias
from ..genre.model_factory import to_models as to_genre_models
from ..utils import is_aldecimal
from . import repository
from .model import Game
from .schema import STEAM_ID, SaveGame


def _create_model(session: Session, game: SaveGame) -> Game:
    return Game(
        steam_id=game["steam_id"],
        name=game["name"],
        released_at=datetime.fromtimestamp(game["released_at"]),
        genres=to_genre_models(session, game["genres"]),
        aliases=[],
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
        game.genres = query.genres
        models[game.steam_id] = game


def _update_aliases(session: Session, game: Game, aliases: set[str]):
    # remove aliases
    existed_aliases: list[str] = []
    for game_alias in game.aliases:
        if game_alias.name not in aliases:
            session.delete(game_alias)
        else:
            existed_aliases.append(game_alias.name)

    # add aliases
    for alias_name in aliases:
        if alias_name not in existed_aliases:
            game.aliases.append(GameAlias(name=alias_name))


def _allow_alias_name(alias_name: str):
    return all(c == " " or is_aldecimal(c) for c in alias_name)


def to_models(session: Session, games: Iterable[SaveGame]) -> list[Game]:
    models = _create_models(session, games)
    _attach_models(session, models)

    for game in games:
        model = models[game["steam_id"]]
        aliases = set(alias_name.lower() for alias_name in game["aliases"] if _allow_alias_name(alias_name))
        _update_aliases(session, model, aliases)

    return list(models.values())
