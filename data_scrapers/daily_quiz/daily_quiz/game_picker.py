import random
from collections import defaultdict
from datetime import datetime
from typing import Iterable, Sequence

from ..aws_lambda.model import Game
from ..config import setting
from .utils import divide_randomly

GameGroup = list[Game]


def _categorize_games_by_genre(games: Iterable[Game], genres: Iterable[str]) -> list[GameGroup]:
    categorized: dict[str, GameGroup] = defaultdict(list)

    for game in games:
        for genre in game.genres:
            if genre not in genres:
                continue

            categorized[genre].append(game)

    return list(categorized.values())


def _filter_older_games(games: Iterable[Game], threshold_released_at: datetime) -> list[Game]:
    return [game for game in games if game.released_at <= threshold_released_at]


def _filter_newer_games(games: Iterable[Game], threshold_released_at: datetime) -> list[Game]:
    return [game for game in games if game.released_at > threshold_released_at]


def _get_median_released_at(games: Iterable[Game]) -> datetime:
    released_ats = [game.released_at for game in games]
    released_ats.sort()
    return released_ats[len(released_ats) // 2]


def _pick_older_newer_games(
    categorized_games: Sequence[GameGroup], median_released_at: datetime
) -> tuple[list[GameGroup], list[GameGroup]]:
    older_part, newer_part = divide_randomly(categorized_games, setting.OLDER_GAME_COUNT)

    olders = [_filter_older_games(games, median_released_at) for games in older_part]
    newers = [_filter_newer_games(games, median_released_at) for games in older_part]

    return olders, newers


def _pick_unique_per_category(categorized_games: Iterable[GameGroup]) -> set[Game]:
    unique_games: set[Game] = set()

    for games in categorized_games:
        games_ = list(set(games) - unique_games)
        game = random.choice(games_)
        unique_games.add(game)

    return unique_games


def pick_games(
    games: Iterable[Game],
    genres: Iterable[str],
):
    categorized_games = _categorize_games_by_genre(games, genres)

    # 오래된 게임 / 최신 게임으로 분리
    median_released_at = _get_median_released_at(games)
    olders, newers = _pick_older_newer_games(categorized_games, median_released_at)

    # 최종 게임 선발
    return _pick_unique_per_category(categorized_games)
