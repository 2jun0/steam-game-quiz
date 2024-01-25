import ast
import csv
import pathlib
import sys
from typing import Sequence, TypedDict

from sqlalchemy.orm import Session

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from private.database import engine  # noqa: E402
from private.game import service  # noqa: E402


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


def save_games(games: Sequence[Game]):
    with Session(engine) as session:
        service.save_games(
            session,
            [
                {
                    "name": game["name"],
                    "steam_id": game["steamId"],
                    "kr_name": None,
                    "released_at": game["releaseDate"] / 1000,
                    "genres": game["genres"],  # type: ignore
                }
                for game in games
            ],
        )

        session.commit()


if __name__ == "__main__":
    with open("filtered_games.csv", "r") as f:
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

    save_games(games)
