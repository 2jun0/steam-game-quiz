import random
from collections import defaultdict
from collections.abc import Collection, Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Union

from ..aws_lambda.model import Game
from ..config import setting
from .exception import NotEnoughGamesError
from .utils import divide_randomly

GameGroup = list[Game]


@dataclass(unsafe_hash=True)
class Category:
    genre: str
    released_at: Union[Literal["older"], Literal["newer"], None] = None


@dataclass
class CategorizedGameGroup:
    category: Category
    games: list[Game]


def _categorize_games_by_genre(games: Iterable[Game], genres: Iterable[str]) -> list[CategorizedGameGroup]:
    categorized: dict[str, GameGroup] = defaultdict(list)

    for game in games:
        for genre in game.genres:
            if genre not in genres:
                continue

            categorized[genre].append(game)

    return [CategorizedGameGroup(category=Category(genre=genre), games=games) for genre, games in categorized.items()]


def _filter_older_games(games: Iterable[Game], threshold_released_at: datetime) -> list[Game]:
    return [game for game in games if game.released_at <= threshold_released_at]


def _filter_newer_games(games: Iterable[Game], threshold_released_at: datetime) -> list[Game]:
    return [game for game in games if game.released_at > threshold_released_at]


def _get_median_released_at(games: Iterable[Game]) -> datetime:
    released_ats = [game.released_at for game in games]
    released_ats.sort()
    return released_ats[len(released_ats) // 2]


def _pick_older_newer_games(
    categorized_games: Sequence[CategorizedGameGroup], median_released_at: datetime
) -> tuple[list[CategorizedGameGroup], list[CategorizedGameGroup]]:
    older_part, newer_part = divide_randomly(categorized_games, setting.OLDER_GAME_COUNT)

    olders = [
        CategorizedGameGroup(
            category=Category(genre=group.category.genre, released_at="older"),
            games=_filter_older_games(group.games, median_released_at),
        )
        for group in older_part
    ]
    newers = [
        CategorizedGameGroup(
            category=Category(genre=group.category.genre, released_at="newer"),
            games=_filter_newer_games(group.games, median_released_at),
        )
        for group in newer_part
    ]

    return olders, newers


def _pick_unique_per_category(categorized_groups: Iterable[CategorizedGameGroup]) -> dict[Category, Game]:
    unique_games: set[Game] = set()
    unique_per_category: dict[Category, Game] = {}

    for group in sorted(categorized_groups, key=lambda g: len(g.games)):
        games_ = list(set(group.games) - unique_games)

        if len(games_) == 0:
            flat = [g for g in group.games for group in categorized_groups]
            raise NotEnoughGamesError(
                f"게임의 수가 너무 적어 게임 선택 알고리즘을 작동할 수 없습니다. 지금까지 선발된 게임: {set(flat)}"
            )

        game = random.choice(games_)
        unique_games.add(game)
        unique_per_category[group.category] = game

    return unique_per_category


def _validate_final_games(games: Collection, genres: Collection):
    if len(games) != len(genres):
        raise NotEnoughGamesError(
            f"게임의 수가 너무 적어 게임 선택 알고리즘을 작동할 수 없습니다. 최종 선발된 게임: {games}"
        )


FEATURE = str


def discribe_feature(games: dict[Category, Game]) -> dict[FEATURE, Game]:
    return {f"{cate.released_at} {cate.genre}": game for cate, game in games.items()}


def pick_games(
    games: Iterable[Game],
    genres: Sequence[str],
) -> dict[FEATURE, Game]:
    categorized_games = _categorize_games_by_genre(games, genres)

    # 오래된 게임 / 최신 게임으로 분리
    median_released_at = _get_median_released_at(games)
    olders, newers = _pick_older_newer_games(categorized_games, median_released_at)

    # 최종 게임 선발
    final_games = _pick_unique_per_category(olders + newers)
    _validate_final_games(final_games, genres)

    return discribe_feature(final_games)
