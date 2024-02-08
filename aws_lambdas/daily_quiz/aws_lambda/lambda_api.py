import json
from typing import Any, Iterable

import boto3

from daily_quiz.aws_lambda.model import Game

from .. import protocols
from ..config import setting
from .event import Event
from .exception import AWSLambdaException
from .model import SaveGameScreenshot, SaveQuiz


class LambdaAPI(protocols.LambdaAPI):
    def __init__(self) -> None:
        self.client = boto3.client("lambda")

    def invoke_lambda(self, event: Event) -> Any:
        response = self.client.invoke(FunctionName=setting.DATABASE_LAMBDA_NAME, Payload=json.dumps(event))

        if "FunctionError" in response:
            raise AWSLambdaException(response["FunctionError"])

        payload: Any = response["Payload"].read().decode("utf-8")
        return json.loads(payload)

    def save_screenshots(self, screenshots: Iterable[SaveGameScreenshot]):
        event = Event(name="save_screenshots", payload=[s.model_dump() for s in screenshots])
        self.invoke_lambda(event)

    def save_quizzes(self, quizzes: Iterable[SaveQuiz]):
        event = Event(name="save_quizzes", payload=[q.model_dump() for q in quizzes])
        self.invoke_lambda(event)

    def get_all_games(self) -> list[Game]:
        event = Event(name="get_all_games", payload=None)
        res = self.invoke_lambda(event)
        return [Game(**g) for g in res]
