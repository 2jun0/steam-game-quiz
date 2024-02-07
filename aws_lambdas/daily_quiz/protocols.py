from typing import Protocol, Sequence

from .aws_lambda.model import Game, SaveGameScreenshot, SaveQuiz
from .steam.model import SteamGameScreenshotResponse


class SteamAPI(Protocol):
    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]:
        ...


class LambdaAPI(Protocol):
    def save_screenshots(self, screenshots: Sequence[SaveGameScreenshot]):
        ...

    def save_quizzes(self, quizzes: Sequence[SaveQuiz]):
        ...

    def get_all_games(self) -> list[Game]:
        ...
