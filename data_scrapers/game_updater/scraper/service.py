from ..protocols import LambdaAPI, SteamAPI
from . import game as game_scraper


def scrap_games(steam_api: SteamAPI, lambda_api: LambdaAPI) -> None:
    game_scraper.scrap_games(steam_api, lambda_api)
