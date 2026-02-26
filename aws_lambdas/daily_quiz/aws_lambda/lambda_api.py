"""
ORIGINAL IMPLEMENTATION
원본 구현 코드

This file contains the original production implementation.
It is preserved for historical/architectural reference only.

This implementation is NOT used in the archive runtime.
It may still be used in the main (production) branch.

이 파일은 원본 프로덕션 구현 코드를 담고 있습니다.
역사적/아키텍처적 참조를 위해 보존됩니다.

아카이브 런타임에서는 사용되지 않으며,
main 브랜치(프로덕션)에서는 여전히 사용될 수 있습니다.
"""

import json
from collections.abc import Iterable
from typing import Any

import boto3

from daily_quiz.aws_lambda.model import Game

from .. import protocols
from ..config import setting
from .event import Event
from .exception import AWSLambdaException
from .model import SaveDailyQuiz, SaveGameScreenshot, SaveQuiz


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

    def save_daily_quizzes(self, daily_quizzes: Iterable[SaveDailyQuiz]):
        event = Event(name="save_daily_quizzes", payload=[q.model_dump() for q in daily_quizzes])
        self.invoke_lambda(event)

    def get_all_games(self) -> list[Game]:
        event = Event(name="get_all_games", payload=None)
        res = self.invoke_lambda(event)
        return [Game(**g) for g in res]
