from collections.abc import Iterable
from typing import Any

from daily_quiz.aws_lambda.model import Game

from .. import protocols
from .event import Event
from .model import SaveDailyQuiz, SaveGameScreenshot, SaveQuiz


class DirectLambdaAPI(protocols.LambdaAPI):
    def invoke_lambda(self, event: Event) -> Any:
        from ...database_lambda.lambda_func import lambda_handler as database_lambda_handler

        return database_lambda_handler(event, None)

    def save_screenshots(self, screenshots: Iterable[SaveGameScreenshot]):
        event = Event(name="save_screenshots", payload=[s.model_dump() for s in screenshots])
        self.invoke_lambda(event)

    def save_quizzes(self, quizzes: Iterable[SaveQuiz]):
        event = Event(name="save_quizzes", payload=[q.model_dump() for q in quizzes])
        self.invoke_lambda(event)

    def save_daily_quizzes(self, daily_quizzes: Iterable[SaveDailyQuiz]):
        event = Event(name="save_daily_quizzes", payload=[q.model_dump() for q in daily_quizzes])
        self.invoke_lambda(event)

    def get_all_games(self) -> list[Game]:
        event = Event(name="get_all_games", payload=None)
        res = self.invoke_lambda(event)
        return [Game(**g) for g in res]
