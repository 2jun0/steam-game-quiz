from typing import Any, Collection, OrderedDict

from sqlalchemy.orm import Session

from . import repository
from .model import Game


def get_some_games(session: Session) -> list[OrderedDict[str, Any]]:
    some_games = repository.get_all_games(session)

    return [g.to_json() for g in some_games]


def save_games(session: Session, games: Collection[dict[str, Any]]):
    games_ = [Game(**game) for game in games]
    session.add_all(games_)


def get_games_in_steam_ids(session: Session, steam_ids: Collection[int]) -> list[OrderedDict[str, Any]]:
    games = repository.get_games_in_steam_ids(session, steam_ids)

    return [g.to_json() for g in games]
