from typing import Sequence

from ..aws_lambda.model import Game
from ..logger import logger
from ..protocols import LambdaAPI, SteamAPI
from .model import NewGameScreenshot


def _remove_existed_new_screenshot(
    lambda_api: LambdaAPI, screenshots: Sequence[NewGameScreenshot]
) -> list[NewGameScreenshot]:
    file_id2screenshot = {s.steam_file_id: s for s in screenshots}
    exists = set(
        s.steam_file_id for s in lambda_api.get_screenshots_in_steam_file_ids(list(file_id2screenshot.keys()))
    )

    return [file_id2screenshot[file_id] for file_id in file_id2screenshot.keys() - exists]


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
