import random
from collections import defaultdict
from collections.abc import Collection, Iterable, Sequence
from datetime import datetime

from ..aws_lambda.model import Game
from ..config import setting
from .exception import NotEnoughGamesError
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
    newers = [_filter_newer_games(games, median_released_at) for games in newer_part]

    return olders, newers


def _pick_unique_per_category(categorized_games: Iterable[GameGroup]) -> set[Game]:
    unique_games: set[Game] = set()

    for games in sorted(categorized_games, key=len):
        games_ = list(set(games) - unique_games)

        if len(games_) == 0:
            flat = [g for g in games for games in categorized_games]
            raise NotEnoughGamesError(
                f"게임의 수가 너무 적어 게임 선택 알고리즘을 작동할 수 없습니다. 지금까지 선발된 게임: {set(flat)}"
            )

        game = random.choice(games_)
        unique_games.add(game)

    return unique_games


def _validate_final_games(games: Collection, genres: Collection):
    if len(games) != len(genres):
        raise NotEnoughGamesError(
            f"게임의 수가 너무 적어 게임 선택 알고리즘을 작동할 수 없습니다. 최종 선발된 게임: {games}"
        )


def pick_games(
    games: Iterable[Game],
    genres: Sequence[str],
) -> set[Game]:
    categorized_games = _categorize_games_by_genre(games, genres)

    # 오래된 게임 / 최신 게임으로 분리
    median_released_at = _get_median_released_at(games)
    olders, newers = _pick_older_newer_games(categorized_games, median_released_at)

    # 최종 게임 선발
    final_games = _pick_unique_per_category(olders + newers)
    _validate_final_games(final_games, genres)
    return final_games
