import json
from typing import Any, Sequence

import boto3

from .. import protocols
from ..config import setting
from ..scraper.model import NewGameScreenshot
from .event import Event
from .exception import AWSLambdaException
from .model import Game, GameScreenshot, SaveGame


class LambdaAPI(protocols.LambdaAPI):
    def __init__(self) -> None:
        self.client = boto3.client("lambda")

    def invoke_lambda(self, event: Event) -> Any:
        response = self.client.invoke(FunctionName=setting.DATABASE_LAMBDA_NAME, Payload=json.dumps(event))

        if "FunctionError" in response:
            raise AWSLambdaException(response["FunctionError"])

        payload: Any = response["Payload"].read().decode("utf-8")
        return json.loads(payload)

    def get_some_games(self) -> list[Game]:
        event = Event(name="get_some_games", payload=None)

        games: list[dict[str, Any]] = self.invoke_lambda(event)
        return [Game(**g) for g in games]

    def get_games_in_steam_ids(self, steam_ids: Sequence[int]) -> list[Game]:
        event = Event(name="get_games_in_steam_ids", payload=steam_ids)

        games: list[dict[str, Any]] = self.invoke_lambda(event)
        return [Game(**g) for g in games]

    def get_screenshots_in_steam_file_ids(self, steam_file_ids: Sequence[int]) -> list[GameScreenshot]:
        event = Event(name="get_screenshots_in_steam_file_ids", payload=steam_file_ids)

        screenshots: list[dict[str, Any]] = self.invoke_lambda(event)
        return [GameScreenshot(**s) for s in screenshots]

    def save_games(self, games: Sequence[SaveGame]):
        event = Event(name="save_games", payload=[g.model_dump() for g in games])

        self.invoke_lambda(event)

    def save_screenshots(self, screenshots: Sequence[NewGameScreenshot]):
        event = Event(name="save_screenshots", payload=[s.model_dump() for s in screenshots])

        self.invoke_lambda(event)
