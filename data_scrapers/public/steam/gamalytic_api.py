from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict

import requests
from typing_extensions import NotRequired


class Game(TypedDict):
    name: str
    steamId: int
    reviews: int
    reviewScore: float
    avgPlaytime: float
    price: float
    copiesSold: int
    revenue: float
    earlyAccess: bool
    developers: list[str]
    publishers: list[str]
    genres: list[str]
    tags: list[str]
    features: list[str]
    EAReleaseDate: NotRequired[int]
    releaseDate: int
    publisherClass: str
    id: int


class GameDetails(Game):
    bizModel: str
    weeklyHistogram: list
    alsoPlayed: list
    win: bool
    mac: bool
    linux: bool
    unreleased: bool
    mature: bool
    followers: int
    owners: int
    players: int
    steamPercent: int
    estimateDetails: dict
    wishlists: int
    predictions: dict
    history: list
    audienceOverlap: list


def get_steam_games(page: int) -> list[Game]:
    res = requests.get(f"https://api.gamalytic.com/steam-games/list?limit=100&page={page}")
    res.raise_for_status()
    res_json = res.json()

    return res_json["result"]


def get_game_details(steam_id: int) -> GameDetails:
    res = requests.get(f"https://api.gamalytic.com/game/{steam_id}")
    res.raise_for_status()
    return res.json()


def get_all_steam_games(worker_cnt: int) -> list[Game]:
    res = requests.get("https://api.gamalytic.com/steam-games/list")
    res.raise_for_status()
    pages = res.json()["pages"]

    games: list[Game] = []
    with ThreadPoolExecutor(worker_cnt) as executer:
        for rs in executer.map(get_steam_games, range(pages)):
            games.extend(rs)

    return games
