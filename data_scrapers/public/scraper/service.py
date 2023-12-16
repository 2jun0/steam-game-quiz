from typing import Collection

from ..logger import logger
from ..model import Game, NewGame, NewGameScreenshot
from ..protocols import LambdaAPI, SteamAPI
from ..steam.exception import SteamAPINoContentsException


def _put_kor_name_in_new_game(steam_api: SteamAPI, game: NewGame) -> None:
    try:
        game_detail = steam_api.get_game_details(game.steam_id, language="korean")
        game.kr_name = game_detail.name
    except SteamAPINoContentsException:
        pass  # game.kr_name will none


def _remove_existed_new_games(lambda_api: LambdaAPI, games: Collection[NewGame]) -> list[NewGame]:
    steam_id2game = {g.steam_id: g for g in games}
    exists = set(g.steam_id for g in lambda_api.get_games_in_steam_ids(list(steam_id2game.keys())))

    return [steam_id2game[steam_id] for steam_id in steam_id2game.keys() - exists]


def _remove_existed_new_screenshot(
    lambda_api: LambdaAPI, screenshots: Collection[NewGameScreenshot]
) -> list[NewGameScreenshot]:
    file_id2screenshot = {s.steam_file_id: s for s in screenshots}
    exists = set(
        s.steam_file_id for s in lambda_api.get_screenshots_in_steam_file_ids(list(file_id2screenshot.keys()))
    )

    return [file_id2screenshot[file_id] for file_id in file_id2screenshot.keys() - exists]


def scrap_games(steam_api: SteamAPI, lambda_api: LambdaAPI) -> None:
    games: list[NewGame] = []

    # get feature games
    logger.info("getting feature games")
    for g in steam_api.get_feature_games():
        games.append(NewGame(steam_id=g.app_id, name=g.name))
    logger.info("feature games: %s", games)

    # remove existed games
    logger.info("removing existed games")
    new_games = _remove_existed_new_games(lambda_api, games)
    logger.info("remain games: %s", new_games)

    # update korean game name
    logger.info("updating korean game name")
    for game in new_games:
        _put_kor_name_in_new_game(steam_api, game)
    logger.info("updated games: %s", new_games)

    # save new games
    lambda_api.save_games(new_games)
    logger.info("saved games: %s", new_games)


def scrap_game_screenshot(steam_api: SteamAPI, lambda_api: LambdaAPI, game: Game) -> None:
    # get some screenshots
    logger.info("getting some screenshots of game: %s", game)
    screenshots: list[NewGameScreenshot] = []

    for s in steam_api.get_game_screenshots(game.steam_id):
        screenshots.append(NewGameScreenshot(steam_file_id=s.file_id, url=s.full_image_url, game_id=game.id))
    logger.info("some screenshots: %s", screenshots)

    # remove existed screenshot
    logger.info("removing existed screenshots")
    new_screenshots = _remove_existed_new_screenshot(lambda_api, screenshots)
    logger.info("remain screenshots: %s", new_screenshots)

    # save new screenshots
    lambda_api.save_screenshots(new_screenshots)
    logger.info("saved screenshots: %s", new_screenshots)


def scrap_game_screenshot_for_all(steam_api: SteamAPI, lambda_api: LambdaAPI) -> None:
    games = lambda_api.get_some_games()

    for game in games:
        scrap_game_screenshot(steam_api, lambda_api, game)
