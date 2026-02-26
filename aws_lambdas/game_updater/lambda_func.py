from typing import Any


def lambda_handler(event: Any, context: Any):

    from game_updater.aws_lambda.direct_lambda_api import DirectLambdaAPI
    from game_updater import protocols
    from game_updater.logger import logger
    from game_updater.scraper.service import update_games
    from game_updater.steam.steam_api import SteamAPI

    def scrap_games_job(lambda_api: protocols.LambdaAPI):
        logger.info("-- scrap game job start -- ")

        update_games(SteamAPI(), lambda_api)

        logger.info("-- scrap game job end -- ")

    lambda_api = DirectLambdaAPI()
    scrap_games_job(lambda_api)
