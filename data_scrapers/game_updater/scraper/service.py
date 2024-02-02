from ..protocols import LambdaAPI, SteamAPI
from . import game as game_scraper
from . import screenshot as screenshot_scraper


def scrap_games(steam_api: SteamAPI, lambda_api: LambdaAPI) -> None:
    game_scraper.scrap_games(steam_api, lambda_api)


def scrap_game_screenshot_for_all(steam_api: SteamAPI, lambda_api: LambdaAPI) -> None:
    games = lambda_api.get_some_games()

    for game in games:
        screenshot_scraper.scrap_game_screenshot(steam_api, lambda_api, game)
