import datetime
import random

import pytest

from daily_quiz.aws_lambda.model import Game
from daily_quiz.config import setting
from daily_quiz.daily_quiz.exception import NotEnoughGamesError
from daily_quiz.daily_quiz.game_picker import pick_games
from tests.daily_quiz.utils.model import create_random_game

OLDER_RELEASED_AT = datetime.datetime(year=1990, month=1, day=14)
NEWER_RELEASED_AT = datetime.datetime(year=2025, month=1, day=14)
DEFAULT_GENRES = [
    "Action",
    "Adventure",
    "Massively Multiplayer",
    "Strategy",
    "RPG",
]


def random_older_games(genres: list[str]) -> list[Game]:
    games = []
    for day in range(1, 3):
        older_released_at = datetime.datetime(year=1990, month=1, day=day)
        games.append(create_random_game(genres=genres, released_at=older_released_at))

    return games


def random_newer_games(genres: list[str]) -> list[Game]:
    games = []
    for day in range(1, 3):
        newer_released_at = datetime.datetime(year=2025, month=1, day=day)
        games.append(create_random_game(genres=genres, released_at=newer_released_at))

    return games


def random_older_newer_games(genres: list[str]) -> list[Game]:
    return [*random_older_games(genres), *random_newer_games(genres)]


def test_pick_games은_입력한_게임에서_장르별로_1개씩_선택해야_한다():
    genres = DEFAULT_GENRES
    games = [
        *random_older_newer_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
        *random_older_newer_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy"]),
        *random_older_newer_games(genres=["Action", "Adventure", "Massively Multiplayer"]),
        *random_older_newer_games(genres=["Action", "Adventure"]),
        *random_older_newer_games(genres=["Action"]),
    ]

    picked = pick_games(games, genres)

    assert len(picked) == len(genres)


def test_pick_games은_장르별_유일한_게임을_선택할_수_없을경우_예외를_던져야한다():
    genres = DEFAULT_GENRES
    games = [
        *random_older_newer_games(genres=["Action", "Adventure"]),
        *random_older_newer_games(genres=["Action", "Adventure"]),
        *random_older_newer_games(genres=["Action", "Adventure"]),
        *random_older_newer_games(genres=["Action", "Adventure"]),
        *random_older_newer_games(genres=["Action", "Adventure"]),
    ]

    with pytest.raises(NotEnoughGamesError):
        pick_games(games, genres)


def test_pick_games은_오래된_혹은_신규_게임을_선택할_수_없는경우_예외가_발생할_수_있다():
    # 예외가 항상 발생하는 극단적인 상황에 대해서만 다룹니다.
    genres = DEFAULT_GENRES
    games = [
        *random_newer_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
        *random_newer_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
        *random_newer_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
        *random_newer_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
        *random_newer_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
    ]

    with pytest.raises(NotEnoughGamesError):
        pick_games(games, genres)

    games = [
        *random_older_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
        *random_older_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
        *random_older_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
        *random_older_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
        *random_older_games(genres=["Action", "Adventure", "Massively Multiplayer", "Strategy", "RPG"]),
    ]

    with pytest.raises(NotEnoughGamesError):
        pick_games(games, genres)


@pytest.mark.parametrize("older_cnt", (0, 2, 5))
def test_pick_games은_older개수_설정이_변경되어도_적응해야한다(older_cnt: int):
    setting.OLDER_GAME_COUNT = older_cnt

    genres = DEFAULT_GENRES
    games = []
    for k in range(1, 4):
        games.extend([create_random_game(genres=random.sample(genres, k=k)) for i in range(100)])

    picked = pick_games(games, genres)

    assert len(picked) == len(genres)
