from collections.abc import Iterable
from typing import Protocol

from .aws_lambda.model import Game, SaveDailyQuiz, SaveGameScreenshot, SaveQuiz
from .steam.model import SteamGameScreenshotResponse


class SteamAPI(Protocol):
    def get_game_screenshots(self, app_id: int, page: int = 1) -> list[SteamGameScreenshotResponse]: ...


class LambdaAPI(Protocol):
    def save_screenshots(self, screenshots: Iterable[SaveGameScreenshot]): ...

    def save_quizzes(self, quizzes: Iterable[SaveQuiz]): ...

    def get_all_games(self) -> list[Game]: ...

    def save_daily_quizzes(self, daily_quizzes: Iterable[SaveDailyQuiz]): ...
