import csv
from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict

import requests
from tqdm import tqdm


class Game(TypedDict):
    name: str
    steamId: int
    reviews: int
    reviewScore: int
    avgPlaytime: int
    price: int
    copiesSold: int
    revenue: int
    earlyAccess: bool
    developers: list[str]
    publishers: list[str]
    genres: list[str]
    tags: list[str]
    features: list[str]
    EAReleaseDate: int
    releaseDate: int
    publisherClass: str
    id: int


def get_steam_games(page: int) -> list[Game]:
    url = f"https://api.gamalytic.com/steam-games/list?limit=100&page={page}"
    res = requests.get(url)
    res.raise_for_status()
    res_json = res.json()

    return res_json["result"]


def scrap_games(worker_cnt: int):
    res = requests.get("https://api.gamalytic.com/steam-games/list")
    res.raise_for_status()
    pages = res.json()["pages"]

    games: list[Game] = []
    with ThreadPoolExecutor(worker_cnt) as executer:
        for rs in tqdm(executer.map(get_steam_games, range(pages)), total=pages):
            games.extend(rs)

    return games


if __name__ == "__main__":
    games = scrap_games(10)

    with open("games.csv", "w") as f:
        csv_f = csv.DictWriter(f, Game.__annotations__.keys())

        csv_f.writerows(games)
