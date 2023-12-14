import json
from typing import Any, Collection

import boto3

from ..model import Game, GameScreenshot, NewGame, NewGameScreenshot
from .event import Event


class LambdaAPI:
    def __init__(self, private_function_name: str) -> None:
        self.private_function_name = private_function_name
        self.client = boto3.client("lambda")

    def invoke_lambda(self, event: Event) -> Any:
        response = self.client.invoke(FunctionName=self.private_function_name, Payload=json.dumps(event))

        payload: Any = response["Payload"].read().decode("utf-8")
        return json.loads(payload)

    def get_some_games(self) -> list[Game]:
        event = Event(name="get_some_games", payload=None)

        games: list[dict[str, Any]] = self.invoke_lambda(event)
        return [Game(**g) for g in games]

    def get_games_in_steam_ids(self, steam_ids: Collection[int]) -> list[Game]:
        event = Event(name="get_games_in_steam_ids", payload=steam_ids)

        games: list[dict[str, Any]] = self.invoke_lambda(event)
        return [Game(**g) for g in games]

    def get_screenshots_in_steam_file_ids(self, steam_file_ids: Collection[int]) -> list[GameScreenshot]:
        event = Event(name="get_screenshots_in_steam_file_ids", payload=steam_file_ids)

        screenshots: list[dict[str, Any]] = self.invoke_lambda(event)
        return [GameScreenshot(**s) for s in screenshots]

    def save_games(self, games: Collection[NewGame]):
        event = Event(name="save_games", payload=games)

        self.invoke_lambda(event)

    def save_screenshots(self, screenshots: Collection[NewGameScreenshot]):
        event = Event(name="save_screenshots", payload=screenshots)

        self.invoke_lambda(event)
