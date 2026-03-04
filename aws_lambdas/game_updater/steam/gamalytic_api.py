from concurrent.futures import ThreadPoolExecutor
from typing import Optional, TypedDict

import requests
from typing_extensions import NotRequired

class Game(TypedDict):
    name: str
    steamId: int
    reviews: int
    reviewScore: float
    price: float
    copiesSold: int
    earlyAccess: bool
    developers: list[str]
    publishers: list[str]
    genres: list[str]
    EAReleaseDate: NotRequired[int]
    releaseDate: int
    firstReleaseDate: int
    publisherClass: str
    id: int


def get_steam_games(page: int) -> list[Game]:
    res = requests.get(f"https://api.gamalytic.com/steam-games/list?limit=100&page={page}")
    res.raise_for_status()
    res_json = res.json()

    return res_json["result"]


def get_all_steam_games(worker_cnt: int, filter_tag: Optional[str] = None) -> list[Game]:
    if filter_tag:
        res = requests.get(f"https://api.gamalytic.com/steam-games/list&tags={filter_tag}")
    else:
        res = requests.get("https://api.gamalytic.com/steam-games/list")
    res.raise_for_status()
    pages = res.json()["pages"]

    games: list[Game] = []
    with ThreadPoolExecutor(worker_cnt) as executer:
        for rs in executer.map(get_steam_games, range(pages)):
            games.extend(rs)

    return games
