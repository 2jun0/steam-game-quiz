import ast
import csv
from typing import Sequence, TypedDict


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
    EAReleaseDate: int
    releaseDate: int
    publisherClass: str
    id: int


MIN_REVENUE = 10000000  # 10M


def is_popular(game: Game) -> bool:
    return game["revenue"] >= MIN_REVENUE


def is_not_sexual(game: Game, sex_games: Sequence[Game]) -> bool:
    return not any(sex_game["steamId"] == game["steamId"] for sex_game in sex_games)


def filter_games(games: Sequence[Game], sex_games: Sequence[Game]) -> list[Game]:
    filtered = []

    for game in games:
        if not is_popular(game):
            continue

        if not is_not_sexual(game, sex_games):
            continue

        if game["steamId"] == 900883:
            continue

        filtered.append(game)

    return filtered


if __name__ == "__main__":
    sex_games: list[Game] = []
    with open("sex_games.csv", "r") as f:
        fieldnames: list[str] = Game.__annotations__.keys()  # type: ignore
        reader = csv.DictReader(f, fieldnames)

        for sex_game in reader:
            for k, v in sex_game.items():
                if sex_game[k]:
                    if Game.__annotations__[k].__name__ == "list":
                        sex_game[k] = ast.literal_eval(v)
                    else:
                        sex_game[k] = Game.__annotations__[k](v)
                else:
                    sex_game[k] = None

            sex_games.append(sex_game)  # type: ignore

    with open("games.csv", "r") as f:
        fieldnames: list[str] = Game.__annotations__.keys()  # type: ignore
        reader = csv.DictReader(f, fieldnames)

        games: list[Game] = []

        for game in reader:
            for k, v in game.items():
                if game[k]:
                    if Game.__annotations__[k].__name__ == "list":
                        game[k] = ast.literal_eval(v)
                    else:
                        game[k] = Game.__annotations__[k](v)
                else:
                    game[k] = None

            games.append(game)  # type: ignore

        games = filter_games(games, sex_games)

    with open("filtered_games.csv", "w") as f:
        writer = csv.DictWriter(f, Game.__annotations__.keys())

        writer.writerows(games)
