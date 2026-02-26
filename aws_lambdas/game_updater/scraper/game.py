import random
from typing import Optional, Sequence

from ..config import setting
from ..logger import logger
from ..protocols import SteamAPI
from .model import Game


def _scrap_all_steam_games(steam_api: SteamAPI, worker_cnt: int, filter_tag: Optional[str] = None) -> list[Game]:
    games = steam_api.get_all_games_from_gamalytic(worker_cnt, filter_tag)
    return [
        Game(
            steam_id=game.app_id,
            name=game.name,
            released_at=game.released_at,
            genres=game.genres,
            tags=game.tags,
            revenue=game.revenue,
        )
        for game in games
    ]


def _is_popular(game: Game) -> bool:
    return game.revenue >= setting.MIN_REVENUE


def _is_not_sexual(game: Game, sex_games: Sequence[Game]) -> bool:
    return not any(sex_game.steam_id == game.steam_id for sex_game in sex_games)


def _filter_games(games: Sequence[Game], sex_games: Sequence[Game]) -> list[Game]:
    filtered = []

    for game in games:
        if not _is_popular(game):
            continue
        if not _is_not_sexual(game, sex_games):
            continue
        if game.steam_id == 900883:  # Elder Scroll 4 Edition
            continue

        filtered.append(game)

    return filtered


def scrap_games(steam_api: SteamAPI) -> list[Game]:
    # get all steam games
    logger.info("getting all steam games")
    games = _scrap_all_steam_games(steam_api, setting.WORKER_CNT)
    logger.info("getting sexual content steam games")
    sex_games = _scrap_all_steam_games(steam_api, setting.WORKER_CNT, filter_tag="NSFW")
    logger.info("game cnt: %d", len(games))
    logger.debug("sample games: %s", random.sample(games, min(len(games), 5)))

    # filter games
    logger.info("filtering games")
    games = _filter_games(games, sex_games)
    logger.info("game cnt: %s", len(games))
    logger.debug("sample games: %s", random.sample(games, min(len(games), 5)))

    return games
