from sqlalchemy.orm import Session

from . import steam_api
from .model import Game


def _put_kor_name_in_game(game: Game) -> None:
    response = steam_api.get_game_details(game.steam_id, language="korean")

    game_details = response[str(game.steam_id)]["data"]
    kr_name = game_details["name"]

    game.kr_name = kr_name


def scrap_games(session: Session) -> None:
    games = []

    # get top 100 games in 2 weeks
    response = steam_api.get_top_100_games_in_2weeks()
    for str_steam_id, detail in response.items():
        game = Game(steam_id=int(str_steam_id), name=detail["name"])
        games.append(game)

    # update korean game name
    for game in games:
        _put_kor_name_in_game(game)

    session.add_all(games)
