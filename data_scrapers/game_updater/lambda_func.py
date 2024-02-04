from typing import Any

from game_updater.aws_lambda.lambda_api import LambdaAPI
from game_updater.logger import logger
from game_updater.scraper.service import scrap_games
from game_updater.steam.steam_api import SteamAPI


def scrap_games_job(lambda_api: LambdaAPI):
    logger.info("-- scrap game job start -- ")

    scrap_games(SteamAPI(), lambda_api)

    logger.info("-- scrap game job end -- ")


def lambda_handler(event: Any, context: Any):
    lambda_api = LambdaAPI()

    scrap_games_job(lambda_api)
