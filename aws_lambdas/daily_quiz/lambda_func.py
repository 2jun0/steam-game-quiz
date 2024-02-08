from typing import Any


def lambda_handler(event: Any, context: Any):

    from daily_quiz import protocols
    from daily_quiz.aws_lambda.lambda_api import LambdaAPI
    from daily_quiz.daily_quiz.serivce import new_daily_quizzes as new_daily_quizzes_
    from daily_quiz.logger import logger
    from daily_quiz.steam.steam_api import SteamAPI

    def new_daily_quizzes(lambda_api: protocols.LambdaAPI, steam_api: protocols.SteamAPI):
        logger.info("-- new daily quizzes job start --")

        new_daily_quizzes_(lambda_api, steam_api)

        logger.info("-- new daily quizzes job end --")

    lambda_api = LambdaAPI()
    steam_api = SteamAPI()

    new_daily_quizzes(lambda_api, steam_api)
